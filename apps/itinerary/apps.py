"""
Itinerary app configuration.
Core app for generating and managing travel itineraries.
"""

from django.apps import AppConfig


class ItineraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.itinerary'
    verbose_name = 'Itinerary Management'
