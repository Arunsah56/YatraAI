"""
URL configuration for locations app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, HiddenGemViewSet, TransportOptionViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'hidden-gems', HiddenGemViewSet, basename='hidden-gem')
router.register(r'transport', TransportOptionViewSet, basename='transport')

urlpatterns = [
    path('', include(router.urls)),
]
