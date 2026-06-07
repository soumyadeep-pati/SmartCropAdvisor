import requests
from django.conf import settings


def get_weather(city):

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={settings.WEATHER_API_KEY}"
        "&units=metric"
    )

    response = requests.get(url)

    return response.json()