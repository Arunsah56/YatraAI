"""
Serializers for tips app.
Convert model instances to/from JSON for API.
"""

from rest_framework import serializers
from .models import BudgetTip, SeasonalTip, LocalExperience


class BudgetTipSerializer(serializers.ModelSerializer):
    """Serializer for BudgetTip model."""
    
    class Meta:
        model = BudgetTip
        fields = [
            'id', 'title', 'category', 'budget_level', 'content',
            'tip_shorthand', 'effectiveness_score', 'relevant_location',
            'created_at'
        ]
        read_only_fields = ['created_at']


class SeasonalTipSerializer(serializers.ModelSerializer):
    """Serializer for SeasonalTip model."""
    
    season_display = serializers.CharField(source='get_season_display', read_only=True)
    
    class Meta:
        model = SeasonalTip
        fields = [
            'id', 'season', 'season_display', 'month', 'title',
            'description', 'temperature_range_celsius', 'rainfall_level',
            'visibility', 'risks', 'recommendations', 'crowd_level',
            'ideal_activities', 'created_at'
        ]
        read_only_fields = ['created_at']


class LocalExperienceSerializer(serializers.ModelSerializer):
    """Serializer for LocalExperience model."""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = LocalExperience
        fields = [
            'id', 'name', 'location', 'location_name', 'category',
            'description', 'what_to_expect', 'duration_hours',
            'cost_per_person_npr', 'group_capacity', 'available_months',
            'booking_required', 'contact_info', 'kids_friendly',
            'physical_difficulty', 'rating', 'created_at'
        ]
        read_only_fields = ['created_at']
