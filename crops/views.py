from django.shortcuts import render, redirect, get_object_or_404
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
            form.save()
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