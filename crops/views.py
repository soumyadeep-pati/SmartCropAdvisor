from django.shortcuts import render, redirect, get_object_or_404
from .forms import SoilDataForm
from .models import SoilData, CropPrediction
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from weather.services import get_weather
from ml.prediction import predict_crop
from django.db.models import Avg, Count
from django.http import HttpResponse

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
    soil_records_list = SoilData.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(soil_records_list, 10)
    page_number = request.GET.get('page')
    soil_records = paginator.get_page(page_number)
    latest_soil = soil_records_list.first()

    return render(
        request,
        'crops/dashboard.html',
        {'soil_records': soil_records, 'latest_soil': latest_soil}
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

    weather = get_weather(soil.location)

    if not weather["success"]:
        return render(
            request,
            "crops/prediction.html",
            {
                "error": weather.get(
                    "message",
                    "Unable to fetch weather data."
                )
            }
        )

    temperature = weather["temperature"]
    humidity = weather["humidity"]

    try:
        crop, confidence = predict_crop(
            soil.nitrogen,
            soil.phosphorus,
            soil.potassium,
            temperature,
            humidity,
            soil.ph,
            soil.rainfall
        )
    except Exception:
        return render(
            request,
            "crops/prediction.html",
            {
                "error": "The AI model is currently unavailable. Please try again later."
            }
        )

    # Save prediction
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
            "soil": soil,
            "weather": weather,
            "temperature": temperature,
            "humidity": humidity,
        }
    )

@login_required
def prediction_history(request):
    predictions = (
        CropPrediction.objects
        .filter(user=request.user)
        .select_related('soil_data')
        .order_by('-created_at')
    )

    total_predictions = predictions.count()

    avg_confidence = predictions.aggregate(
        Avg('confidence')
    )['confidence__avg']

    top_crop = (
        predictions
        .values('crop_name')
        .annotate(total=Count('crop_name'))
        .order_by('-total')
        .first()
    )

    crop_distribution = list(
        predictions
        .values('crop_name')
        .annotate(total=Count('crop_name'))
        .order_by('-total')
    )

    chart_labels = [crop['crop_name'] for crop in crop_distribution]
    chart_data = [crop['total'] for crop in crop_distribution]

    chart_context = {
        'labels': chart_labels,
        'data': chart_data,
    }

    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    prediction_rows = []

    for prediction in page_obj:
        confidence_percent = None

        if prediction.confidence is not None:
            confidence_percent = round(
                prediction.confidence * 100
            )

        prediction_rows.append({
            'prediction': prediction,
            'confidence_percent': confidence_percent,
        })

    return render(
        request,
        'crops/prediction_history.html',
        {
            'prediction_rows': prediction_rows,
            'page_obj': page_obj,
            'total_predictions': total_predictions,
            'avg_confidence': avg_confidence,
            'top_crop': top_crop,
            'chart_data': chart_context,
        }
    )


@login_required
def download_prediction_report(request, prediction_id):

    prediction = get_object_or_404(
        CropPrediction,
        id=prediction_id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; '
        f'filename="prediction_{prediction.id}.pdf"'
    )

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Smart Crop Advisor Report",
            styles['Title']
        )
    )

    content.append(Spacer(1, 20))

    soil = prediction.soil_data

    content.append(
        Paragraph(
            f"Crop: {prediction.crop_name}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Location: {soil.location}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Nitrogen: {soil.nitrogen}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Phosphorus: {soil.phosphorus}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Potassium: {soil.potassium}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"pH: {soil.ph}",
            styles['Normal']
        )
    )

    confidence_text = (
        f"Confidence: {prediction.confidence:.2f}"
        if prediction.confidence is not None
        else "Confidence: N/A"
    )
    content.append(
        Paragraph(confidence_text, styles['Normal'])
    )

    doc.build(content)

    return response