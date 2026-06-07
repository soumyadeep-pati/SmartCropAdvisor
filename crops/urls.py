from django.urls import path
from .views import add_soil_data, dashboard, delete_soil_data, edit_soil_data, home, predict_crop_view

urlpatterns = [
    path('', home, name='home'),
    path('soil/add/', add_soil_data, name='add_soil'),
    path('dashboard/', dashboard, name='dashboard'),
    path('soil/<int:pk>/edit/', edit_soil_data, name='edit_soil'),
    path('soil/<int:pk>/delete/', delete_soil_data, name='delete_soil'),
    path(
    'predict/<int:pk>/',
    predict_crop_view,
    name='predict_crop'
),
]
