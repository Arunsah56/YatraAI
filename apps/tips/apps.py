"""
Tips app configuration.
Manages travel tips, seasonal advice, and local recommendations.
"""

from django.apps import AppConfig


class TipsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tips'
    verbose_name = 'Tips Management'
