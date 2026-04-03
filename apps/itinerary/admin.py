"""
Admin configuration for itinerary app.
Register models for Django admin interface.
"""

from django.contrib import admin
from .models import Itinerary, ItineraryDay, ItineraryActivity, ItineraryNote


class ItineraryDayInline(admin.TabularInline):
    """Inline admin for itinerary days."""
    model = ItineraryDay
    extra = 0
    fields = ('day_number', 'title', 'location', 'accommodation_type')
    readonly_fields = ('created_at',)


class ItineraryActivityInline(admin.TabularInline):
    """Inline admin for itinerary activities."""
    model = ItineraryActivity
    extra = 0
    fields = ('order', 'time_start', 'activity_type', 'name', 'estimated_cost_npr', 'importance_level')


class ItineraryNoteInline(admin.TabularInline):
    """Inline admin for itinerary notes."""
    model = ItineraryNote
    extra = 0
    fields = ('title', 'note_type', 'is_pinned')
    readonly_fields = ('created_at',)


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'destination_primary', 'number_of_days', 'budget_level',
        'group_size', 'status', 'estimated_total_budget_npr', 'created_at'
    )
    list_filter = (
        'status', 'budget_level', 'created_at', 'travelers_type',
        'destination_primary'
    )
    search_fields = ('title', 'description', 'destination_primary__name')
    readonly_fields = ('created_at', 'updated_at', 'ai_response', 'ai_prompt')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status')
        }),
        ('Trip Details', {
            'fields': (
                'destination_primary', 'number_of_days', 'interests',
                'budget_level', 'estimated_total_budget_npr', 'budget_breakdown'
            )
        }),
        ('Traveler Information', {
            'fields': ('group_size', 'travelers_type')
        }),
        ('AI Generation', {
            'fields': ('ai_prompt', 'ai_response'),
            'classes': ('collapse',)
        }),
        ('Session & Metadata', {
            'fields': ('session_id', 'created_at', 'updated_at')
        }),
    )
    
    inlines = [ItineraryDayInline, ItineraryNoteInline]


@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = (
        'itinerary', 'day_number', 'title', 'location',
        'accommodation_type', 'total_daily_budget_npr'
    )
    list_filter = ('accommodation_type', 'location', 'itinerary__budget_level')
    search_fields = ('title', 'description', 'location__name', 'itinerary__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Day Information', {
            'fields': ('itinerary', 'day_number', 'title', 'location')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Accommodation', {
            'fields': (
                'accommodation_name', 'accommodation_type',
                'accommodation_estimated_cost_npr'
            )
        }),
        ('Budget Breakdown', {
            'fields': (
                'meals_budget_npr', 'activities_budget_npr',
                'transport_budget_npr'
            )
        }),
        ('Activities & Notes', {
            'fields': ('activities', 'travel_notes', 'packing_tips', 'local_tips')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [ItineraryActivityInline]


@admin.register(ItineraryActivity)
class ItineraryActivityAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'day', 'activity_type', 'time_start', 'time_end',
        'estimated_cost_npr', 'importance_level', 'order'
    )
    list_filter = (
        'activity_type', 'importance_level', 'day__itinerary',
        'related_location'
    )
    search_fields = ('name', 'description', 'location_description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('day', 'order', 'name', 'activity_type')
        }),
        ('Timing', {
            'fields': ('time_start', 'time_end', 'duration_minutes')
        }),
        ('Description & Location', {
            'fields': ('description', 'location_description')
        }),
        ('References', {
            'fields': ('related_location', 'related_hidden_gem')
        }),
        ('Cost & Importance', {
            'fields': ('estimated_cost_npr', 'importance_level')
        }),
        ('Tips', {
            'fields': ('tips',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ItineraryNote)
class ItineraryNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'itinerary', 'note_type', 'is_pinned', 'created_at')
    list_filter = ('note_type', 'is_pinned', 'created_at', 'itinerary')
    search_fields = ('title', 'content', 'itinerary__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Note Information', {
            'fields': ('itinerary', 'title', 'note_type', 'is_pinned')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
