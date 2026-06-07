from django.shortcuts import render
from .services import get_weather
from django.contrib import messages


def weather_view(request):
    city = "Kolkata"
    weather = None
    error = None

    try:
        weather_data = get_weather(city)
        
        # Check if the API returned an error
        if 'main' in weather_data:
            weather = weather_data
        else:
            error = weather_data.get('message', 'Unable to fetch weather data')
    except Exception as e:
        error = f"Error fetching weather: {str(e)}"

    return render(
        request,
        "weather/weather.html",
        {"weather": weather, "city": city, "error": error}
    )