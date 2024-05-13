
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from products.views import professionals



from products.views import ItemView
from rest_framework import routers

route = routers.DefaultRouter()
route.register(r'items', ItemView, basename='itemview')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(route.urls)),
    path('api/', include('users.urls')),
    path('api/stripe/',include('payments.urls')),
    path('api/mpesa/',include('payments.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('professionals/', professionals, name='professionals')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



