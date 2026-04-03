"""
Serializers for locations app.
Convert model instances to/from JSON for API.
"""

from rest_framework import serializers
from .models import Location, HiddenGem, TransportOption


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model."""
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'region', 'description', 'altitude',
            'latitude', 'longitude', 'best_time_visit', 'weather_info',
            'distance_from_kathmandu_km', 'travel_time_hours',
            'primary_attraction', 'popularity_score', 'created_at'
        ]
        read_only_fields = ['created_at']


class LocationDetailSerializer(LocationSerializer):
    """Detailed serializer with related objects."""
    
    hidden_gems = serializers.SerializerMethodField()
    
    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ['hidden_gems']
    
    def get_hidden_gems(self, obj):
        gems = obj.hidden_gems.all()[:5]  # Limit to 5
        return HiddenGemSerializer(gems, many=True).data


class HiddenGemSerializer(serializers.ModelSerializer):
    """Serializer for HiddenGem model."""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = HiddenGem
        fields = [
            'id', 'name', 'location', 'location_name', 'gem_type',
            'description', 'why_special', 'accessibility_level',
            'entry_fee_npr', 'entry_fee_foreigner_npr', 'best_time_visit',
            'visit_duration_hours', 'crowd_level', 'rating', 'created_at'
        ]
        read_only_fields = ['created_at']


class TransportOptionSerializer(serializers.ModelSerializer):
    """Serializer for TransportOption model."""
    
    source_name = serializers.CharField(source='source.name', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    
    class Meta:
        model = TransportOption
        fields = [
            'id', 'source', 'source_name', 'destination', 'destination_name',
            'transport_type', 'distance_km', 'duration_hours', 'local_cost_npr',
            'local_cost_description', 'comfort_level', 'frequency', 'operator',
            'booking_required', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']
