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


def station(request, station_id):
    station = Station.objects.all().filter(station_id=station_id)[0]
    station_name = station.get_name()
    station_fleet = Vehicle.objects.filter(station=station_id)

    template = 'station.html'
    context = {
        'station_name': station_name,
        'station_id': station_id,
        'station_fleet': station_fleet,
        'img_src': 'https://via.placeholder.com/150x100.png',
        'vehicle_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    }

    return render(request, template, context)


def vehicle(request, station_id, vehicle_path):

    station = Station.objects.all().filter(station_id=station_id)[0]
    station_name = station.get_name()
    station_path = station.get_path()

    vehicle_name = vehicle_path.replace('_', ' ')  # TODO I don't like this part.
    vehicle_name = vehicle_name.capitalize()       # TODO Create vehicle_id field instead?
    vehicle = Vehicle.objects.filter(name=vehicle_name)[0]

    vehicle_bags = vehicle.vehicletobagassociation_set.all()
    new_column_cutoffs = ['ETT Side',
                          'Under Syringes',
                          'Left Outside Pocket',
                          'Top Outside Pouches',
                          'Top Outside Flap',
                          'Inside Bag Main']
    context = {
        'vehicle_bags': vehicle_bags,
        'station_name': station_name,
        'station_path': station_path,
        'station_id': station_id,
        'vehicle_name': vehicle_name,
        'vehicle_path': vehicle_path,
        'new_column_cutoffs': new_column_cutoffs
    }
    template = 'vehicle.html'

    return render(request, template, context)
