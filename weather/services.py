import requests
from django.conf import settings


def get_weather(city):
    if not settings.WEATHER_API_KEY:
        return {
            "success": False,
            "message": "Weather API key is missing. Add WEATHER_API_KEY to your .env file."
        }

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            url,
            params={"q": city, "appid": settings.WEATHER_API_KEY, "units": "metric"},
            timeout=10
        )
        data = response.json()
    except requests.RequestException:
        return {
            "success": False,
            "message": "Could not connect to the weather service. Please try again."
        }

    except ValueError:
        return {
            "success": False,
            "message": "Weather service returned an invalid response."
        }

    if response.status_code != 200:
        return {
            "success": False,
            "message": data.get("message", "Unknown error")
        }

    return {
        "success": True,
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "main": data["weather"][0]["main"],
        "wind_speed": data["wind"]["speed"],
    }
