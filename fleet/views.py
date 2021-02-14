from django.shortcuts import render
from .models import Station


def home(request):
    stations = Station.objects.all()
    template = 'home.html'
    context = {
        'stations': stations,
        'img_src': 'https://via.placeholder.com/150x100.png'
    }

    return render(request, template, context)
