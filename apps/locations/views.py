"""
Views for locations app.
REST API endpoints for locations, hidden gems, and transport.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Location, HiddenGem, TransportOption
from .serializers import (
    LocationSerializer,
    LocationDetailSerializer,
    HiddenGemSerializer,
    TransportOptionSerializer
)


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Location model.
    Provides list and detail views for Nepal destinations.
    """
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'region', 'primary_attraction']
    ordering_fields = ['name', 'distance_from_kathmandu_km', 'popularity_score']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return LocationDetailSerializer
        return LocationSerializer
    
    @action(detail=False, methods=['GET'])
    def by_region(self, request):
        """Get locations filtered by region."""
        region = request.query_params.get('region')
        if not region:
            return Response(
                {'error': 'region parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        locations = self.queryset.filter(region=region)
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def by_altitude(self, request):
        """Get locations filtered by altitude."""
        altitude = request.query_params.get('altitude')
        if not altitude:
            return Response(
                {'error': 'altitude parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        locations = self.queryset.filter(altitude=altitude)
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def popular(self, request):
        """Get most popular locations."""
        limit = int(request.query_params.get('limit', 10))
        locations = self.queryset.order_by('-popularity_score')[:limit]
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)


class HiddenGemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for HiddenGem model.
    Provides endpoints for discovering hidden gems and local secrets.
    """
    
    queryset = HiddenGem.objects.select_related('location').order_by('-rating')
    serializer_class = HiddenGemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'gem_type', 'location__name']
    ordering_fields = ['rating', 'visit_duration_hours', 'accessibility_level']
    ordering = ['-rating']
    
    @action(detail=False, methods=['GET'])
    def by_type(self, request):
        """Filter hidden gems by type."""
        gem_type = request.query_params.get('type')
        if not gem_type:
            return Response(
                {'error': 'type parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        gems = self.queryset.filter(gem_type=gem_type)
        serializer = self.get_serializer(gems, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def by_location(self, request):
        """Get hidden gems for a specific location."""
        location_id = request.query_params.get('location_id')
        if not location_id:
            return Response(
                {'error': 'location_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        gems = self.queryset.filter(location_id=location_id)
        serializer = self.get_serializer(gems, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def least_crowded(self, request):
        """Get least crowded hidden gems."""
        limit = int(request.query_params.get('limit', 5))
        gems = self.queryset.filter(crowd_level='low')[:limit]
        serializer = self.get_serializer(gems, many=True)
        return Response(serializer.data)


class TransportOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for TransportOption model.
    Provides endpoints for finding transport between locations.
    """
    
    queryset = TransportOption.objects.select_related('source', 'destination')
    serializer_class = TransportOptionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['source__name', 'destination__name', 'transport_type', 'operator']
    ordering_fields = ['duration_hours', 'local_cost_npr', 'comfort_level']
    ordering = ['duration_hours']
    
    @action(detail=False, methods=['GET'])
    def route(self, request):
        """Get transport options for a specific route."""
        source_id = request.query_params.get('source_id')
        destination_id = request.query_params.get('destination_id')
        
        if not source_id or not destination_id:
            return Response(
                {'error': 'source_id and destination_id parameters required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        options = self.queryset.filter(
            source_id=source_id,
            destination_id=destination_id
        )
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def by_type(self, request):
        """Filter transport by type."""
        transport_type = request.query_params.get('type')
        if not transport_type:
            return Response(
                {'error': 'type parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        options = self.queryset.filter(transport_type=transport_type)
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def cheapest_route(self, request):
        """Find cheapest transport for a route."""
        source_id = request.query_params.get('source_id')
        destination_id = request.query_params.get('destination_id')
        
        if not source_id or not destination_id:
            return Response(
                {'error': 'source_id and destination_id parameters required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        options = self.queryset.filter(
            source_id=source_id,
            destination_id=destination_id
        ).order_by('local_cost_npr')[:1]
        
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)


def locations_view(request):
    """Frontend view for locations."""
    locations = Location.objects.all()
    return render(request, 'locations.html', {'locations': locations})
