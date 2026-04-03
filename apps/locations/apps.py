"""
Locations app configuration.
Manages Nepal-specific locations and destinations.
"""

from django.apps import AppConfig


class LocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.locations'
    verbose_name = 'Locations Management'
