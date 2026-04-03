"""
Views for itinerary app.
REST API endpoints for generating and managing travel itineraries.
"""

import json
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .models import Itinerary, ItineraryDay, ItineraryActivity
from .serializers import (
    ItinerarySerializer,
    ItineraryDetailSerializer,
    ItineraryGenerationRequestSerializer,
    ItineraryDaySerializer,
    ItineraryActivitySerializer
)
from .services import ItineraryAIService
from apps.locations.models import Location, HiddenGem, TransportOption
from apps.tips.models import BudgetTip, SeasonalTip, LocalExperience

logger = logging.getLogger(__name__)


class ItineraryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Itinerary model.
    Provides endpoints for generating, retrieving, and managing itineraries.
    """
    
    queryset = Itinerary.objects.all().order_by('-created_at')
    serializer_class = ItinerarySerializer
    
    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return ItineraryDetailSerializer
        return ItinerarySerializer
    
    def get_queryset(self):
        """Filter by session_id if provided."""
        queryset = self.queryset
        session_id = self.request.query_params.get('session_id')
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset
    
    @action(detail=False, methods=['POST'])
    def generate(self, request):
        """
        Generate a new itinerary using AI.
        
        Request body:
        {
            "destination": "Kathmandu",
            "number_of_days": 5,
            "budget_level": "mid",
            "interests": ["trekking", "culture"],
            "group_size": 1,
            "travelers_type": "solo"
        }
        """
        
        # Validate request
        serializer = ItineraryGenerationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        destination_name = validated_data['destination']
        
        try:
            # Get destination location
            location = Location.objects.get(name__iexact=destination_name)
            
            # Gather local data for AI context
            location_data = self._gather_location_data(location)
            transport_data = self._gather_transport_data(location)
            tips_data = self._gather_tips_data(
                validated_data['budget_level'],
                validated_data['interests']
            )
            
            # Generate itinerary using AI
            ai_service = ItineraryAIService()
            ai_result = ai_service.generate_itinerary(
                destination=destination_name,
                number_of_days=validated_data['number_of_days'],
                budget_level=validated_data['budget_level'],
                interests=validated_data['interests'],
                group_size=validated_data['group_size'],
                travelers_type=validated_data['travelers_type'],
                location_data=location_data,
                transport_data=transport_data,
                tips_data=tips_data
            )
            
            if not ai_result['success']:
                return Response(
                    {'error': 'Failed to generate itinerary'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Create itinerary record
            with transaction.atomic():
                itinerary = self._create_itinerary_from_ai(
                    location=location,
                    ai_data=ai_result['data'],
                    validated_data=validated_data,
                    ai_prompt=self._build_prompt_string(validated_data, location_data),
                    ai_response=ai_result['data']
                )
                
                # Parse and create itinerary days and activities
                self._populate_itinerary_days(itinerary, ai_result['data'])
            
            serializer = ItineraryDetailSerializer(itinerary)
            return Response(
                {
                    'success': True,
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        except Location.DoesNotExist:
            return Response(
                {'error': f"Location '{destination_name}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            return Response(
                {'error': f"Failed to generate itinerary: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['POST'])
    def save(self, request, pk=None):
        """Save an itinerary."""
        itinerary = self.get_object()
        itinerary.status = 'saved'
        itinerary.save()
        
        serializer = self.get_serializer(itinerary)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def export(self, request, pk=None):
        """Export itinerary as JSON."""
        itinerary = self.get_object()
        serializer = ItineraryDetailSerializer(itinerary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def recent(self, request):
        """Get recently generated itineraries."""
        limit = int(request.query_params.get('limit', 10))
        itineraries = self.queryset[:limit]
        serializer = self.get_serializer(itineraries, many=True)
        return Response(serializer.data)
    
    def _gather_location_data(self, location: Location) -> dict:
        """Gather local location context for AI."""
        return {
            'name': location.name,
            'region': location.get_region_display(),
            'description': location.description,
            'altitude': location.get_altitude_display(),
            'best_time': location.best_time_visit,
            'weather': location.weather_info,
            'primary_attraction': location.primary_attraction,
            'distance_from_kathmandu_km': location.distance_from_kathmandu_km,
        }
    
    def _gather_transport_data(self, location: Location) -> list:
        """Gather transport options for AI context."""
        routes = TransportOption.objects.filter(
            source=location
        )[:5]
        
        return [
            {
                'route': f"{t.source.name} → {t.destination.name}",
                'type': t.get_transport_type_display(),
                'duration_hours': t.duration_hours,
                'cost_npr': t.local_cost_npr,
                'frequency': t.frequency,
            }
            for t in routes
        ]
    
    def _gather_tips_data(self, budget_level: str, interests: list) -> dict:
        """Gather relevant tips for AI context."""
        budget_tips = BudgetTip.objects.filter(
            budget_level__in=[budget_level, 'all']
        ).order_by('-effectiveness_score')[:3]
        
        return {
            'budget_tips': [
                {'title': t.title, 'tip': t.tip_shorthand}
                for t in budget_tips
            ],
            'current_season': SeasonalTip.objects.filter(
                month=1  # This should be current month in production
            ).first() and {
                'season': SeasonalTip.objects.get(month=1).get_season_display(),
                'advice': SeasonalTip.objects.get(month=1).recommendations
            }
        }
    
    def _build_prompt_string(self, data: dict, location_data: dict) -> str:
        """Build a string representation of the prompt sent to AI."""
        return f"""Generate itinerary for {data.get('destination', location_data.get('name', 'Nepal'))}, 
{data['number_of_days']} days, {data['budget_level']} budget,  
interests: {', '.join(data['interests'])}, 
group: {data['group_size']} {data['travelers_type']}(s)"""
    
    def _create_itinerary_from_ai(
        self,
        location: Location,
        ai_data: dict,
        validated_data: dict,
        ai_prompt: str,
        ai_response: dict
    ) -> Itinerary:
        """Create Itinerary record from AI response."""
        
        return Itinerary.objects.create(
            title=ai_data.get('title', f"Trip to {location.name}"),
            description=ai_data.get('summary', ''),
            destination_primary=location,
            number_of_days=validated_data['number_of_days'],
            budget_level=validated_data['budget_level'],
            interests=validated_data['interests'],
            estimated_total_budget_npr=ai_data.get('estimated_total_budget_npr', 0),
            budget_breakdown=ai_data.get('budget_breakdown', {}),
            group_size=validated_data['group_size'],
            travelers_type=validated_data['travelers_type'],
            status='generated',
            ai_prompt=ai_prompt,
            ai_response=ai_response,
            session_id=self.request.session.session_key or 'unknown'
        )
    
    def _populate_itinerary_days(self, itinerary: Itinerary, ai_data: dict) -> None:
        """Parse AI response and create ItineraryDay and Activity records."""
        
        for day_data in ai_data.get('days', []):
            day_number = day_data.get('day_number', 0)
            
            # Get location for the day
            day_location = None
            try:
                day_location = Location.objects.get(
                    name__icontains=day_data.get('location', '')
                )
            except Location.DoesNotExist:
                pass
            
            # Create day record
            day = ItineraryDay.objects.create(
                itinerary=itinerary,
                day_number=day_number,
                location=day_location,
                title=day_data.get('title', f"Day {day_number}"),
                description=day_data.get('description', ''),
                accommodation_name=day_data.get('accommodation', {}).get('name', ''),
                accommodation_type=day_data.get('accommodation', {}).get('type', 'hotel'),
                accommodation_estimated_cost_npr=day_data.get('accommodation', {}).get(
                    'estimated_cost_npr', 0
                ),
                meals_budget_npr=day_data.get('meals_budget_npr', 0),
                activities_budget_npr=day_data.get('activities_budget_npr', 0),
                transport_budget_npr=day_data.get('transport_budget_npr', 0),
                activities=day_data.get('activities', []),
                travel_notes=day_data.get('travel_notes', ''),
                packing_tips=day_data.get('packing_tips', ''),
                local_tips=day_data.get('local_tips', '')
            )
            
            # Create activity records for each activity
            for idx, activity_data in enumerate(day_data.get('activities', []), 1):
                ItineraryActivity.objects.create(
                    day=day,
                    time_start=activity_data.get('time_start'),
                    time_end=activity_data.get('time_end'),
                    activity_type=activity_data.get('type', 'sightseeing'),
                    name=activity_data.get('name', ''),
                    description=activity_data.get('description', ''),
                    location_description=activity_data.get('location', ''),
                    estimated_cost_npr=activity_data.get('estimated_cost_npr', 0),
                    duration_minutes=activity_data.get('duration_minutes'),
                    tips=activity_data.get('tips', ''),
                    importance_level=activity_data.get('importance_level', 'recommended'),
                    order=idx
                )


# Frontend Views
@require_http_methods(["GET"])
def index_view(request):
    """Homepage with itinerary generation form."""
    locations = Location.objects.all().values_list('name', flat=True)
    context = {
        'locations': locations,
        'interests': ['Adventure', 'Culture', 'Trekking', 'Relaxation', 'Spiritual', 'Food']
    }
    return render(request, 'index.html', context)


@require_http_methods(["GET"])
def results_view(request, itinerary_id):
    """Display generated itinerary."""
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    context = {
        'itinerary': itinerary,
        'days': itinerary.days.all()
    }
    return render(request, 'results.html', context)


@require_http_methods(["GET"])
def explore_view(request):
    """Explore hidden gems and local experiences."""
    gems = HiddenGem.objects.all()[:12]
    experiences = LocalExperience.objects.all()[:12]
    context = {
        'hidden_gems': gems,
        'experiences': experiences
    }
    return render(request, 'explore.html', context)
