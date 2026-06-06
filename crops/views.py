from django.shortcuts import render

def home(request):
    return render(request, 'crops/home.html')