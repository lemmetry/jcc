from django.shortcuts import render
from .models import Station


def home(request):
    stations = Station.objects.all()
    template = 'home.html'
    context = {
        'stations': stations
    }

    return render(request, template, context)
