"""
Itinerary models for managing travel plans.
Core models for generating and storing itineraries.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Itinerary(models.Model):
    """
    Main itinerary model that stores generated travel plans.
    Contains all details about a trip including days, budget, and activities.
    """
    
    BUDGET_LEVEL_CHOICES = [
        ('low', 'Budget (< NPR 2000/day)'),
        ('mid', 'Mid-range (NPR 2000-5000/day)'),
        ('luxury', 'Luxury (> NPR 5000/day)'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('saved', 'Saved'),
        ('completed', 'Completed'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Trip Parameters
    destination_primary = models.ForeignKey(
        'locations.Location',
        on_delete=models.SET_NULL,
        null=True,
        related_name='itineraries_primary'
    )
    number_of_days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(365)])
    budget_level = models.CharField(max_length=20, choices=BUDGET_LEVEL_CHOICES)
    
    # Interests
    interests = models.JSONField(
        default=list,
        help_text="List of interests: adventure, culture, trekking, relaxation, etc."
    )
    
    # Estimated Budget
    estimated_total_budget_npr = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    budget_breakdown = models.JSONField(
        default=dict,
        blank=True,
        help_text="Breakdown: accommodation, food, transport, activities, etc."
    )
    
    # Traveler Info
    group_size = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=1
    )
    travelers_type = models.CharField(
        max_length=50,
        choices=[
            ('solo', 'Solo'),
            ('couple', 'Couple'),
            ('family', 'Family'),
            ('group', 'Group'),
        ],
        default='solo'
    )
    
    # Generated Content
    ai_prompt = models.TextField(blank=True, help_text="The prompt sent to OpenAI")
    ai_response = models.JSONField(
        default=dict,
        blank=True,
        help_text="Raw response from OpenAI API"
    )
    
    # Status & Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Session tracking (for frontend integration)
    session_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['session_id']),
            models.Index(fields=['budget_level']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.number_of_days} days, {self.budget_level})"
    
    @property
    def daily_budget_npr(self):
        """Calculate average daily budget."""
        if self.estimated_total_budget_npr:
            return self.estimated_total_budget_npr // self.number_of_days
        return None


class ItineraryDay(models.Model):
    """
    Individual day within an itinerary.
    Contains activities, accommodations, and details for each day.
    """
    
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Location for this day
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    title = models.CharField(max_length=200, help_text="e.g., 'Kathmandu Exploration'")
    description = models.TextField()
    
    # Accommodation
    accommodation_name = models.CharField(max_length=200, blank=True)
    accommodation_type = models.CharField(
        max_length=50,
        choices=[
            ('hotel', 'Hotel'),
            ('guesthouse', 'Guesthouse'),
            ('homestay', 'Homestay'),
            ('lodge', 'Lodge'),
            ('camping', 'Camping'),
        ],
        blank=True
    )
    accommodation_estimated_cost_npr = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Daily Budget Breakdown
    meals_budget_npr = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    activities_budget_npr = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    transport_budget_npr = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    # Activities
    activities = models.JSONField(
        default=list,
        help_text="List of activities for the day"
    )
    
    # Travel Notes
    travel_notes = models.TextField(blank=True)
    packing_tips = models.TextField(blank=True)
    local_tips = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['itinerary', 'day_number']
        unique_together = ['itinerary', 'day_number']
        indexes = [
            models.Index(fields=['itinerary', 'day_number']),
            models.Index(fields=['location']),
        ]
    
    def __str__(self):
        return f"Day {self.day_number} - {self.title}"
    
    @property
    def total_daily_budget_npr(self):
        """Calculate total budget for this day."""
        total = 0
        if self.accommodation_estimated_cost_npr:
            total += self.accommodation_estimated_cost_npr
        if self.meals_budget_npr:
            total += self.meals_budget_npr
        if self.activities_budget_npr:
            total += self.activities_budget_npr
        if self.transport_budget_npr:
            total += self.transport_budget_npr
        return total


class ItineraryActivity(models.Model):
    """
    Individual activity within a day.
    Detailed breakdown of what to do, where, and when.
    """
    
    ACTIVITY_TYPE_CHOICES = [
        ('sightseeing', 'Sightseeing'),
        ('trekking', 'Trekking'),
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('food', 'Food Tour'),
        ('relaxation', 'Relaxation'),
        ('spiritual', 'Spiritual'),
        ('shopping', 'Shopping'),
        ('nightlife', 'Nightlife'),
    ]
    
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='activity_details')
    
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    location_description = models.CharField(max_length=300, blank=True)
    estimated_cost_npr = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    duration_minutes = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    # References
    related_location = models.ForeignKey(
        'locations.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    related_hidden_gem = models.ForeignKey(
        'tips.LocalExperience',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    tips = models.TextField(blank=True, help_text="Local tips, what to bring, etc.")
    importance_level = models.CharField(
        max_length=20,
        choices=[('must', 'Must-See'), ('recommended', 'Recommended'), ('optional', 'Optional')],
        default='recommended'
    )
    
    order = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day', 'order', 'time_start']
        indexes = [
            models.Index(fields=['day']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"Day {self.day.day_number}: {self.name}"


class ItineraryNote(models.Model):
    """
    Additional notes and reminders for an itinerary.
    For user-added information and custom modifications.
    """
    
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='notes')
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    NOTE_TYPE_CHOICES = [
        ('reminder', 'Reminder'),
        ('warning', 'Warning'),
        ('tip', 'Tip'),
        ('custom', 'Custom Note'),
    ]
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='custom')
    
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['itinerary']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.note_type})"
