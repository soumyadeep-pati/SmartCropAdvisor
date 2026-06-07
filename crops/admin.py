from django.contrib import admin
from .models import SoilData, CropPrediction

# Register your models here.
admin.site.register(SoilData)
admin.site.register(CropPrediction)
