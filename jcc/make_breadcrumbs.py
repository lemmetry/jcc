from django.urls import reverse


def make_home_breadcrumb():
    return {
        'text': 'Home',
        'link': reverse('home')
    }


def make_station_breadcrumb(station):
    return {
        'text': station.get_name(),
        'link': reverse('station orders dashboard', kwargs={
            'station_id': station.station_id
        })
    }


def make_order_breadcrumb(station_order):
    return {
        'text': 'Order #%s' % station_order.pk,
        'link': reverse('make station order', kwargs={
            'order_pk': station_order.pk
        })
    }


def make_vehicle_breadcrumb(vehicle):
    return {'text': vehicle.name}
