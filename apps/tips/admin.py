"""
Admin configuration for tips app.
Register models for Django admin interface.
"""

from django.contrib import admin
from .models import BudgetTip, SeasonalTip, LocalExperience


@admin.register(BudgetTip)
class BudgetTipAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'budget_level', 'effectiveness_score',
        'relevant_location', 'created_at'
    )
    list_filter = ('category', 'budget_level', 'effectiveness_score', 'created_at')
    search_fields = ('title', 'content', 'tip_shorthand')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'budget_level', 'relevant_location')
        }),
        ('Content', {
            'fields': ('content', 'tip_shorthand')
        }),
        ('Rating', {
            'fields': ('effectiveness_score',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SeasonalTip)
class SeasonalTipAdmin(admin.ModelAdmin):
    list_display = (
        'get_season_display', 'month', 'title', 'rainfall_level',
        'visibility', 'crowd_level', 'created_at'
    )
    list_filter = ('season', 'month', 'rainfall_level', 'visibility', 'crowd_level')
    search_fields = ('title', 'description', 'recommendations', 'risks')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('season', 'month', 'title')
        }),
        ('Description', {
            'fields': ('description', 'recommendations')
        }),
        ('Weather Information', {
            'fields': (
                'temperature_range_celsius', 'rainfall_level',
                'visibility'
            )
        }),
        ('Travel Information', {
            'fields': (
                'risks', 'crowd_level', 'ideal_activities'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(LocalExperience)
class LocalExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'location', 'category', 'duration_hours',
        'cost_per_person_npr', 'rating', 'booking_required', 'created_at'
    )
    list_filter = (
        'category', 'location', 'booking_required',
        'kids_friendly', 'physical_difficulty', 'created_at'
    )
    search_fields = ('name', 'description', 'location__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'category', 'rating')
        }),
        ('Description', {
            'fields': ('description', 'what_to_expect')
        }),
        ('Duration & Pricing', {
            'fields': (
                'duration_hours', 'cost_per_person_npr',
                'group_capacity'
            )
        }),
        ('Availability & Booking', {
            'fields': (
                'available_months', 'booking_required',
                'contact_info'
            )
        }),
        ('Details', {
            'fields': (
                'kids_friendly', 'physical_difficulty'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
