from django.shortcuts import render, redirect
from .forms import SoilDataForm
from .models import SoilData

def home(request):
    return render(request, 'crops/home.html')

def add_soil_data(request):

    if request.method == 'POST':
        form = SoilDataForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = SoilDataForm()

    return render(
        request,
        'crops/soil_form.html',
        {'form': form}
    )

def dashboard(request):
    soil_records = SoilData.objects.all().order_by('-created_at')

    return render(
        request,
        'crops/dashboard.html',
        {'soil_records': soil_records}
    )