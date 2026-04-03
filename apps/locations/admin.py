"""
Admin configuration for locations app.
Register models for Django admin interface.
"""

from django.contrib import admin
from .models import Location, HiddenGem, TransportOption


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'region', 'altitude', 'distance_from_kathmandu_km',
        'popularity_score', 'created_at'
    )
    list_filter = ('region', 'altitude', 'created_at')
    search_fields = ('name', 'description', 'primary_attraction')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'region', 'description', 'primary_attraction')
        }),
        ('Geography', {
            'fields': ('altitude', 'latitude', 'longitude')
        }),
        ('Travel Information', {
            'fields': (
                'best_time_visit', 'weather_info', 'distance_from_kathmandu_km',
                'travel_time_hours'
            )
        }),
        ('Metadata', {
            'fields': ('popularity_score', 'created_at', 'updated_at')
        }),
    )


@admin.register(HiddenGem)
class HiddenGemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'location', 'gem_type', 'accessibility_level',
        'rating', 'crowd_level', 'created_at'
    )
    list_filter = ('gem_type', 'crowd_level', 'location', 'created_at')
    search_fields = ('name', 'description', 'location__name')
    readonly_fields = ('created_at', 'updated_at', 'rating')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'gem_type', 'rating')
        }),
        ('Description', {
            'fields': ('description', 'why_special')
        }),
        ('Access Information', {
            'fields': (
                'accessibility_level', 'entry_fee_npr', 'entry_fee_foreigner_npr',
                'visit_duration_hours', 'crowd_level'
            )
        }),
        ('Timing', {
            'fields': ('best_time_visit',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(TransportOption)
class TransportOptionAdmin(admin.ModelAdmin):
    list_display = (
        'source', 'destination', 'transport_type', 'duration_hours',
        'local_cost_npr', 'comfort_level', 'frequency'
    )
    list_filter = ('transport_type', 'comfort_level', 'source', 'destination')
    search_fields = ('source__name', 'destination__name', 'operator')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Route', {
            'fields': ('source', 'destination')
        }),
        ('Transport Details', {
            'fields': (
                'transport_type', 'operator', 'distance_km', 'duration_hours',
                'comfort_level', 'frequency'
            )
        }),
        ('Pricing', {
            'fields': ('local_cost_npr', 'local_cost_description')
        }),
        ('Additional Info', {
            'fields': ('booking_required', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
