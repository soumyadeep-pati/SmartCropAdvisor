from django.urls import path
from .views import dashboard, home, add_soil_data, dashboard    

urlpatterns = [
    path('', home, name='home'),
    path('soil/add/', add_soil_data, name='add_soil'),
    path('dashboard/', dashboard, name='dashboard'),
]