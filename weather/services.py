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

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }