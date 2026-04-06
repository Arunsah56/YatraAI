"""
URL configuration for tips app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BudgetTipViewSet, SeasonalTipViewSet, LocalExperienceViewSet

router = DefaultRouter()
router.register(r'budget-tips', BudgetTipViewSet, basename='budget-tip')
router.register(r'seasonal-tips', SeasonalTipViewSet, basename='seasonal-tip')
router.register(r'local-experiences', LocalExperienceViewSet, basename='local-experience')

urlpatterns = [
    path('', include(router.urls)),
]
