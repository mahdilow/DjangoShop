from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Authentication URLs
    path('accounts/', include('allauth.account.urls')),
    
    # API and REST Auth URLs
    path('api/v1/', include('api.urls')),
    
    
    path('auth/', include('authapp.urls')),
    
    # Swagger URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', 
         SpectacularSwaggerView.as_view(url_name='schema'), 
         name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

