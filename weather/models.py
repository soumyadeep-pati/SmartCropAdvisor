from django.conf import settings
from django.db import models


class WeatherSearch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weather_searches",
    )
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    main = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    wind_speed = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-searched_at"]

    def __str__(self):
        return f"{self.user.username} - {self.city}"
