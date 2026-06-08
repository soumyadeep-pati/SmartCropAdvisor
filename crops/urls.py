from django.urls import path
from .views import add_soil_data, dashboard, delete_soil_data, download_prediction_report, edit_soil_data, home, predict_crop_view, prediction_history

urlpatterns = [
    path('', home, name='home'),
    path('soil/add/', add_soil_data, name='add_soil'),
    path('dashboard/', dashboard, name='dashboard'),
    path('soil/<int:pk>/edit/', edit_soil_data, name='edit_soil'),
    path('soil/<int:pk>/delete/', delete_soil_data, name='delete_soil'),
    path('predict/<int:pk>/', predict_crop_view, name='predict_crop'),
    path('prediction-history/', prediction_history, name='prediction_history'),
    path('prediction-report/<int:prediction_id>/', download_prediction_report, name='download_prediction_report'),
]
