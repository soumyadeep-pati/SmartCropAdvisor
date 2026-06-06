from django.shortcuts import render, redirect
from .forms import SoilDataForm
from .models import SoilData
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'crops/home.html')
@login_required
def add_soil_data(request):

    if request.method == 'POST':
        form = SoilDataForm(request.POST)

        if form.is_valid():
            soil = form.save(commit=False)
            soil.user = request.user
            soil.save()
            return redirect('dashboard')

    else:
        form = SoilDataForm()

    return render(
        request,
        'crops/soil_form.html',
        {'form': form}
    )
@login_required
def dashboard(request):
    soil_records = SoilData.objects.filter(user=request.user).order_by('-created_at')

    return render(
        request,
        'crops/dashboard.html',
        {'soil_records': soil_records}
    )