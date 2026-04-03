"""
Location models for managing Nepal destinations.
Includes locations, hidden gems, and transport options.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):
    """
    Represents a city or major destination in Nepal.
    Used as reference for itinerary generation.
    """
    
    ALTITUDE_CHOICES = [
        ('lowland', 'Lowland (< 500m)'),
        ('mid', 'Mid Hills (500-2000m)'),
        ('highland', 'Highland (2000-4000m)'),
        ('alpine', 'Alpine (> 4000m)'),
    ]
    
    REGION_CHOICES = [
        ('kathmandu', 'Kathmandu Valley'),
        ('northeast', 'Northeast (Ilam, Jhapa)'),
        ('central', 'Central (Pokhara, Chitwan)'),
        ('west', 'West (Dhulikhel, Narayanghat)'),
        ('northwest', 'Northwest (Gorkha, Manang)'),
        ('east', 'East (Bhaktapur, Namobuddha)'),
    ]
    
    name = models.CharField(max_length=100, unique=True, db_index=True)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    description = models.TextField()
    altitude = models.CharField(max_length=20, choices=ALTITUDE_CHOICES)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    best_time_visit = models.CharField(max_length=200, help_text="e.g., October-November")
    weather_info = models.TextField()
    
    # Tourism info
    distance_from_kathmandu_km = models.IntegerField(validators=[MinValueValidator(0)])
    travel_time_hours = models.FloatField(validators=[MinValueValidator(0)])
    primary_attraction = models.CharField(max_length=200)
    
    # Metadata
    popularity_score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1-10 scale"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['region']),
            models.Index(fields=['altitude']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.region})"


class HiddenGem(models.Model):
    """
    Off-beat destinations and lesser-known places in Nepal.
    Enhanced itinerary suggestions with unique experiences.
    """
    
    TYPE_CHOICES = [
        ('natural', 'Natural'),
        ('cultural', 'Cultural'),
        ('adventure', 'Adventure'),
        ('spiritual', 'Spiritual'),
        ('local', 'Local Experience'),
    ]
    
    name = models.CharField(max_length=150, db_index=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='hidden_gems')
    gem_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    description = models.TextField()
    why_special = models.TextField(help_text="What makes this place unique")
    
    # Access info
    accessibility_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Easy, 5=Very Difficult"
    )
    entry_fee_npr = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    entry_fee_foreigner_npr = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    best_time_visit = models.CharField(max_length=200)
    visit_duration_hours = models.FloatField()
    
    crowd_level = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low'
    )
    
    # Rating
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=4.5
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', 'name']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['gem_type']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.location.name}"


class TransportOption(models.Model):
    """
    Transportation methods between locations in Nepal.
    Used for calculating travel logistics and estimates.
    """
    
    TRANSPORT_TYPE_CHOICES = [
        ('bus', 'Bus'),
        ('jeep', 'Jeep/Taxi'),
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('hiking', 'Hiking'),
        ('private_vehicle', 'Private Vehicle'),
    ]
    
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='arrivals')
    
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPE_CHOICES)
    
    # Journey details
    distance_km = models.IntegerField(validators=[MinValueValidator(0)])
    duration_hours = models.FloatField(validators=[MinValueValidator(0)])
    
    # Cost estimation (in NPR)
    local_cost_npr = models.IntegerField(validators=[MinValueValidator(0)])  # Cost for locals/tourists
    local_cost_description = models.CharField(max_length=100, null=True, blank=True)
    
    comfort_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Basic, 5=Luxury"
    )
    frequency = models.CharField(max_length=100, help_text="e.g., 'Daily 6AM-6PM' or 'On demand'")
    
    # Additional info
    operator = models.CharField(max_length=200, null=True, blank=True, help_text="Bus company, airline, etc.")
    booking_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['source', 'destination', 'transport_type']
        unique_together = ['source', 'destination', 'transport_type']
        indexes = [
            models.Index(fields=['source', 'destination']),
            models.Index(fields=['transport_type']),
        ]
    
    def __str__(self):
        return f"{self.source.name} → {self.destination.name} ({self.transport_type})"
