from django.shortcuts import render, redirect, get_object_or_404
from .forms import SoilDataForm
from .models import SoilData, CropPrediction
from django.contrib.auth.decorators import login_required
from weather.services import get_weather
from ml.prediction import predict_crop


def attach_weather_to_soil(soil):
    weather_data = get_weather(soil.location)

    if weather_data["success"]:
        soil.weather_city = weather_data["city"]
        soil.weather_temperature = weather_data["temperature"]
        soil.weather_feels_like = weather_data["feels_like"]
        soil.weather_humidity = weather_data["humidity"]
        soil.weather_pressure = weather_data["pressure"]
        soil.weather_main = weather_data["main"]
        soil.weather_description = weather_data["description"]
        soil.weather_wind_speed = weather_data["wind_speed"]
        soil.weather_error = ""
    else:
        soil.weather_error = weather_data["message"]

def home(request):
    return render(request, 'crops/home.html')

@login_required
def add_soil_data(request):
    if request.method == 'POST':
        form = SoilDataForm(request.POST)
        if form.is_valid():
            soil = form.save(commit=False)
            soil.user = request.user
            attach_weather_to_soil(soil)
            soil.save()
            return redirect('dashboard')
    else:
        form = SoilDataForm()

    return render(
        request,
        'crops/soil_form.html',
        {'form': form, 'title': 'Add Soil Data'}
    )

@login_required
def edit_soil_data(request, pk):
    soil = get_object_or_404(
        SoilData,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = SoilDataForm(request.POST, instance=soil)
        if form.is_valid():
            soil = form.save(commit=False)
            attach_weather_to_soil(soil)
            soil.save()
            return redirect('dashboard')
    else:
        form = SoilDataForm(instance=soil)

    return render(
        request,
        'crops/soil_form.html',
        {'form': form, 'title': 'Edit Soil Data', 'soil': soil}
    )

@login_required
def dashboard(request):
    soil_records = SoilData.objects.filter(user=request.user).order_by('-created_at')

    return render(
        request,
        'crops/dashboard.html',
        {'soil_records': soil_records}
    )

@login_required
def delete_soil_data(request, pk):
    soil = get_object_or_404(
        SoilData,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        soil.delete()
        return redirect('dashboard')

    return render(
        request,
        'crops/delete_confirm.html',
        {'soil': soil}
    )


@login_required
def predict_crop_view(request, pk):

    soil = get_object_or_404(
        SoilData,
        pk=pk,
        user=request.user
    )

    # Use actual weather data if available, fallback to defaults
    temperature = soil.weather_temperature if soil.weather_temperature else 25
    humidity = soil.weather_humidity if soil.weather_humidity else 70
    rainfall = getattr(soil, 'rainfall', 150)
    
    crop, confidence = predict_crop(
        soil.nitrogen,
        soil.phosphorus,
        soil.potassium,
        temperature,
        humidity,
        soil.ph,
        rainfall
    )

    CropPrediction.objects.create(
        user=request.user,
        soil_data=soil,
        crop_name=crop,
        confidence=confidence
    )

    return render(
        request,
        "crops/prediction.html",
        {
            "crop": crop,
            "confidence": confidence,
            "soil": soil
        }
    )

@login_required
def prediction_history(request):

    predictions = CropPrediction.objects.filter(
        user=request.user
    ).select_related('soil_data').order_by('-created_at')

    prediction_rows = []
    for prediction in predictions:
        confidence_percent = None
        if prediction.confidence is not None:
            confidence_percent = round(prediction.confidence * 100)

        prediction_rows.append({
            'prediction': prediction,
            'confidence_percent': confidence_percent,
        })

    return render(
        request,
        'crops/prediction_history.html',
        {
            'prediction_rows': prediction_rows
        }
    )
