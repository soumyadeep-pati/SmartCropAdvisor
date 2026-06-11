from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WeatherSearch
from .services import get_weather


def weather_view(request):
    has_search = "city" in request.GET and request.GET.get("city", "").strip()
    city = request.GET.get("city", "Kolkata").strip()

    if not city:
        city = "Kolkata"

    weather_data = get_weather(city)

    if weather_data["success"]:
        weather = weather_data
        error = None

        if has_search and request.user.is_authenticated:
            WeatherSearch.objects.create(
                user=request.user,
                city=weather_data["city"],
                temperature=weather_data["temperature"],
                feels_like=weather_data["feels_like"],
                humidity=weather_data["humidity"],
                pressure=weather_data["pressure"],
                main=weather_data["main"],
                description=weather_data["description"],
                wind_speed=weather_data["wind_speed"],
            )
            messages.success(request, f"Weather search for {weather_data['city']} saved.")
    else:
        weather = None
        error = weather_data["message"]

    return render(
        request,
        "weather/weather.html",
        {
            "weather": weather,
            "city": city,
            "error": error
        }
    )


@login_required
def weather_history(request):
    searches = WeatherSearch.objects.filter(user=request.user)

    return render(
        request,
        "weather/history.html",
        {"searches": searches}
    )
