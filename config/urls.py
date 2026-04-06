"""
URL Configuration for YatraAI project.
Main URL router that includes all app-specific URLs.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

api_patterns = [
    # API Schema Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # App-specific APIs
    path('api/', include('apps.itinerary.urls')),
    path('api/', include('apps.locations.urls')),
    path('api/', include('apps.tips.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API URLs
    *api_patterns,
    
    # Frontend views (will be added later)
    path('', include('apps.itinerary.urls')),  # Include frontend views
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = 'YatraAI Admin'
admin.site.site_title = 'YatraAI Management'
