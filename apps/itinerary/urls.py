"""
URL configuration for itinerary app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItineraryViewSet, index_view, results_view, explore_view

router = DefaultRouter()
router.register(r'itinerary', ItineraryViewSet, basename='itinerary')

urlpatterns = [
    # Frontend views
    path('', index_view, name='index'),
    path('page/results/<int:itinerary_id>/', results_view, name='results'),
    path('page/explore/', explore_view, name='explore'),
    
    # API endpoints
    path('', include(router.urls)),
]
