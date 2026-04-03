"""
Serializers for itinerary app.
Convert model instances to/from JSON for API.
"""

from rest_framework import serializers
from .models import Itinerary, ItineraryDay, ItineraryActivity, ItineraryNote


class ItineraryActivitySerializer(serializers.ModelSerializer):
    """Serializer for ItineraryActivity model."""
    
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    importance_level_display = serializers.CharField(source='get_importance_level_display', read_only=True)
    
    class Meta:
        model = ItineraryActivity
        fields = [
            'id', 'day', 'time_start', 'time_end', 'activity_type',
            'activity_type_display', 'name', 'description', 'location_description',
            'estimated_cost_npr', 'duration_minutes', 'related_location',
            'related_hidden_gem', 'tips', 'importance_level',
            'importance_level_display', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']


class ItineraryDaySerializer(serializers.ModelSerializer):
    """Serializer for ItineraryDay model."""
    
    activity_details = ItineraryActivitySerializer(many=True, read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True, allow_null=True)
    accommodation_type_display = serializers.CharField(source='get_accommodation_type_display', read_only=True, allow_null=True)
    
    class Meta:
        model = ItineraryDay
        fields = [
            'id', 'itinerary', 'day_number', 'location', 'location_name',
            'title', 'description', 'accommodation_name', 'accommodation_type',
            'accommodation_type_display', 'accommodation_estimated_cost_npr',
            'meals_budget_npr', 'activities_budget_npr', 'transport_budget_npr',
            'total_daily_budget_npr', 'activities', 'travel_notes', 'packing_tips',
            'local_tips', 'activity_details', 'created_at'
        ]
        read_only_fields = ['created_at', 'total_daily_budget_npr']


class ItineraryNoteSerializer(serializers.ModelSerializer):
    """Serializer for ItineraryNote model."""
    
    note_type_display = serializers.CharField(source='get_note_type_display', read_only=True)
    
    class Meta:
        model = ItineraryNote
        fields = [
            'id', 'itinerary', 'title', 'content', 'note_type',
            'note_type_display', 'is_pinned', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ItinerarySerializer(serializers.ModelSerializer):
    """Serializer for Itinerary model."""
    
    destination_primary_name = serializers.CharField(
        source='destination_primary.name',
        read_only=True,
        allow_null=True
    )
    budget_level_display = serializers.CharField(source='get_budget_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    travelers_type_display = serializers.CharField(source='get_travelers_type_display', read_only=True)
    daily_budget_npr = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Itinerary
        fields = [
            'id', 'title', 'description', 'destination_primary',
            'destination_primary_name', 'number_of_days', 'budget_level',
            'budget_level_display', 'interests', 'estimated_total_budget_npr',
            'budget_breakdown', 'group_size', 'travelers_type',
            'travelers_type_display', 'status', 'status_display',
            'daily_budget_npr', 'session_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'daily_budget_npr']


class ItineraryDetailSerializer(ItinerarySerializer):
    """Detailed serializer with related objects."""
    
    days = ItineraryDaySerializer(many=True, read_only=True)
    notes = ItineraryNoteSerializer(many=True, read_only=True)
    
    class Meta(ItinerarySerializer.Meta):
        fields = ItinerarySerializer.Meta.fields + ['days', 'notes', 'ai_prompt', 'ai_response']
        read_only_fields = ItinerarySerializer.Meta.read_only_fields + ['ai_prompt', 'ai_response']


class ItineraryGenerationRequestSerializer(serializers.Serializer):
    """Serializer for itinerary generation request."""
    
    destination = serializers.CharField(max_length=200)
    number_of_days = serializers.IntegerField(min_value=1, max_value=365)
    budget_level = serializers.ChoiceField(choices=['low', 'mid', 'luxury'])
    interests = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        max_length=10
    )
    group_size = serializers.IntegerField(min_value=1, max_value=100, default=1)
    travelers_type = serializers.ChoiceField(
        choices=['solo', 'couple', 'family', 'group'],
        default='solo'
    )
    
    def validate_destination(self, value):
        """Validate that destination exists in database."""
        from apps.locations.models import Location
        if not Location.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(f"Location '{value}' not found.")
        return value
