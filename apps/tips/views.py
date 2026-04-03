"""
Views for tips app.
REST API endpoints for travel tips and seasonal advice.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BudgetTip, SeasonalTip, LocalExperience
from .serializers import (
    BudgetTipSerializer,
    SeasonalTipSerializer,
    LocalExperienceSerializer
)


class BudgetTipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for BudgetTip model.
    Provides money-saving tips for travelers in Nepal.
    """
    
    queryset = BudgetTip.objects.order_by('-effectiveness_score')
    serializer_class = BudgetTipSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'category']
    ordering_fields = ['effectiveness_score', 'category', 'budget_level']
    
    @action(detail=False, methods=['GET'])
    def by_category(self, request):
        """Get tips filtered by category."""
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'error': 'category parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tips = self.queryset.filter(category=category)
        serializer = self.get_serializer(tips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def by_budget(self, request):
        """Get tips for a specific budget level."""
        budget_level = request.query_params.get('budget_level')
        if not budget_level:
            return Response(
                {'error': 'budget_level parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tips = self.queryset.filter(budget_level__in=[budget_level, 'all'])
        serializer = self.get_serializer(tips, many=True)
        return Response(serializer.data)


class SeasonalTipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for SeasonalTip model.
    Provides seasonal advice for Nepal travel.
    """
    
    queryset = SeasonalTip.objects.all().order_by('month')
    serializer_class = SeasonalTipSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'recommendations']
    ordering_fields = ['month', 'season']
    
    @action(detail=False, methods=['GET'])
    def by_season(self, request):
        """Get tips for a specific season."""
        season = request.query_params.get('season')
        if not season:
            return Response(
                {'error': 'season parameter required (spring, summer, autumn, winter)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tips = self.queryset.filter(season=season).order_by('month')
        serializer = self.get_serializer(tips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def current_season(self, request):
        """Get tips for current month."""
        from datetime import datetime
        current_month = datetime.now().month
        
        tips = self.queryset.filter(month=current_month)
        serializer = self.get_serializer(tips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def best_conditions(self, request):
        """Get months with best weather conditions."""
        tips = self.queryset.filter(
            visibility='excellent',
            rainfall_level='low',
            crowd_level='medium'
        )
        serializer = self.get_serializer(tips, many=True)
        return Response(serializer.data)


class LocalExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for LocalExperience model.
    Provides authentic local experiences and cultural activities.
    """
    
    queryset = LocalExperience.objects.select_related('location').order_by('-rating')
    serializer_class = LocalExperienceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category', 'location__name']
    ordering_fields = ['rating', 'cost_per_person_npr', 'physical_difficulty']
    
    @action(detail=False, methods=['GET'])
    def by_category(self, request):
        """Get experiences filtered by category."""
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'error': 'category parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        experiences = self.queryset.filter(category=category)
        serializer = self.get_serializer(experiences, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def by_location(self, request):
        """Get experiences for a specific location."""
        location_id = request.query_params.get('location_id')
        if not location_id:
            return Response(
                {'error': 'location_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        experiences = self.queryset.filter(location_id=location_id)
        serializer = self.get_serializer(experiences, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def kids_friendly(self, request):
        """Get experiences suitable for kids."""
        experiences = self.queryset.filter(kids_friendly=True)
        serializer = self.get_serializer(experiences, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def budget_friendly(self, request):
        """Get budget-friendly experiences (under NPR 1000)."""
        experiences = self.queryset.filter(cost_per_person_npr__lt=1000)
        serializer = self.get_serializer(experiences, many=True)
        return Response(serializer.data)
