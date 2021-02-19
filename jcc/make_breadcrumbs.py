from django.urls import reverse


def make_home_breadcrumb():
    return ['Home', reverse('home')]


def make_station_breadcrumb(station):
    return [station.get_name(), reverse('station orders dashboard',
                                        kwargs={'station_id': station.station_id})
            ]


def make_order_breadcrumb(station_order):
    return ['Order #%s' % station_order.pk, reverse('make station order',
                                                    kwargs={'station_id': station_order.station.station_id,
                                                            'order_pk': station_order.pk})
            ]


def make_vehicle_breadcrumb(vehicle):
    return [vehicle.name, '']
