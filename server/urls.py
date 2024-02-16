
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products.views import ItemView
from rest_framework import routers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

route = routers.DefaultRouter()
route.register(r'items', ItemView, basename='itemview')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(route.urls)),
    path('api/', include('users.urls')),
    path('api/stripe/',include('payments.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
