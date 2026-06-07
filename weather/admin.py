from django.contrib import admin
from .models import WeatherSearch


@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ("city", "user", "temperature", "humidity", "searched_at")
    search_fields = ("city", "user__username")
    list_filter = ("searched_at",)
