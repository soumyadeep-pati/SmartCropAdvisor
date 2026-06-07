
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crops.urls')),
    path('accounts/', include('accounts.urls')),
    path('weather/', include('weather.urls')),
]
