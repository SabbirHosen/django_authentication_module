from django.contrib import admin
from django.conf import settings
from django.contrib.messages import api
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('blogs/', include('blog.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        # YOUR PATTERNS
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
