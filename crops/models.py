from django.contrib.auth.models import User
from django.db import models

class SoilData(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nitrogen = models.IntegerField()
    phosphorus = models.IntegerField()
    potassium = models.IntegerField()
    ph = models.FloatField()
    location = models.CharField(max_length=100)
    weather_city = models.CharField(max_length=100, blank=True)
    weather_temperature = models.FloatField(null=True, blank=True)
    weather_feels_like = models.FloatField(null=True, blank=True)
    weather_humidity = models.IntegerField(null=True, blank=True)
    weather_pressure = models.IntegerField(null=True, blank=True)
    weather_main = models.CharField(max_length=100, blank=True)
    weather_description = models.CharField(max_length=255, blank=True)
    weather_wind_speed = models.FloatField(null=True, blank=True)
    weather_error = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Unknown user"
        return f"{username} - {self.location}"
