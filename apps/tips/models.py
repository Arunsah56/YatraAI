"""
Tips models for travel advice and seasonal information.
Includes budget tips, seasonal advice, and local recommendations.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BudgetTip(models.Model):
    """
    Budget optimization tips for travelers in Nepal.
    Helps generate budget-aware recommendations.
    """
    
    CATEGORY_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('activities', 'Activities'),
        ('shopping', 'Shopping'),
        ('general', 'General'),
    ]
    
    BUDGET_LEVEL_CHOICES = [
        ('budget', 'Budget (< NPR 2000/day)'),
        ('mid', 'Mid-range (NPR 2000-5000/day)'),
        ('luxury', 'Luxury (> NPR 5000/day)'),
        ('all', 'Applicable to All'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    budget_level = models.CharField(max_length=20, choices=BUDGET_LEVEL_CHOICES, default='all')
    
    content = models.TextField()
    tip_shorthand = models.CharField(max_length=100, help_text="Quick version for UI display")
    
    # Effectiveness rating
    effectiveness_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=7,
        help_text="How helpful is this tip? (1-10)"
    )
    
    # Reference location (optional)
    relevant_location = models.ForeignKey(
        'locations.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effectiveness_score', 'category']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['budget_level']),
        ]
    
    def __str__(self):
        return f"{self.category.title()} - {self.title}"


class SeasonalTip(models.Model):
    """
    Seasonal advice and weather-related information for Nepal.
    Used for context-aware itinerary generation.
    """
    
    SEASON_CHOICES = [
        ('spring', 'Spring (Feb-May)'),
        ('summer', 'Summer/Monsoon (Jun-Aug)'),
        ('autumn', 'Autumn (Sep-Nov)'),
        ('winter', 'Winter (Dec-Jan)'),
    ]
    
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        unique_for_month='season'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Environmental info
    temperature_range_celsius = models.CharField(max_length=50, help_text="e.g., '15-25°C'")
    rainfall_level = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    visibility = models.CharField(
        max_length=20,
        choices=[('poor', 'Poor'), ('good', 'Good'), ('excellent', 'Excellent')],
        default='good'
    )
    
    # Travel advice
    risks = models.TextField(blank=True, help_text="e.g., 'Landslides, Flight cancellations'")
    recommendations = models.TextField()
    
    # Travel crowds
    crowd_level = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    # Best activities during this season
    ideal_activities = models.TextField(
        help_text="Comma-separated activities best suited for this season"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['month']
        verbose_name_plural = "Seasonal Tips"
        indexes = [
            models.Index(fields=['season']),
            models.Index(fields=['month']),
        ]
    
    def __str__(self):
        return f"{self.get_season_display()} - {self.title}"


class LocalExperience(models.Model):
    """
    Unique local experiences and cultural activities in Nepal.
    Enriches itineraries with authentic Nepali experiences.
    """
    
    CATEGORY_CHOICES = [
        ('homestay', 'Homestay'),
        ('workshop', 'Workshop/Class'),
        ('festival', 'Festival'),
        ('market', 'Local Market'),
        ('cuisine', 'Cuisine Experience'),
        ('trekking', 'Trekking Guide'),
        ('spiritual', 'Spiritual'),
    ]
    
    name = models.CharField(max_length=200, db_index=True)
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.CASCADE,
        related_name='local_experiences'
    )
    
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    # Duration and pricing
    duration_hours = models.FloatField(validators=[MinValueValidator(0.5)])
    cost_per_person_npr = models.IntegerField(validators=[MinValueValidator(0)])
    
    group_capacity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    # Availability
    available_months = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., '1,2,3,10,11,12' (1=Jan, 12=Dec)"
    )
    booking_required = models.BooleanField(default=True)
    contact_info = models.CharField(max_length=200, blank=True)
    
    # Details
    what_to_expect = models.TextField()
    kids_friendly = models.BooleanField(default=True)
    physical_difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=2,
        help_text="1=Easy, 5=Very Difficult"
    )
    
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=4.5
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', 'category']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category}) - {self.location.name}"
