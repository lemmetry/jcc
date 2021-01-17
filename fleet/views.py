from django.shortcuts import render
from .models import Station
from .models import Vehicle


def home(request):
    stations = Station.objects.all()
    template = 'home.html'
    context = {
        'stations': stations,
        'img_src': 'https://via.placeholder.com/150x100.png',
        'station_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    }

    return render(request, template, context)
