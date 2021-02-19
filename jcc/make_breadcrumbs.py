from django.urls import reverse


def make_home_breadcrumb(home_view):
    return ['Home', reverse(home_view)]


def make_station_breadcrumb(station_view, station):
    return [station.get_name(), reverse(station_view,
                                        kwargs={'station_id': station.station_id})
            ]


def make_order_breadcrumb(station_order_view, station_order):
    return ['Order #%s' % station_order.pk, reverse(station_order_view,
                                                    kwargs={'station_id': station_order.station.station_id,
                                                            'order_pk': station_order.pk})
            ]


def make_vehicle_breadcrumb(vehicle):
    return [vehicle.name, '']
