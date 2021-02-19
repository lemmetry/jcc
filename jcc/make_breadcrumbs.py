from django.urls import reverse


def make_home_breadcrumb_maker(home_view):
    def make():
        return ['Home', reverse(home_view)]
    return make


def make_station_breadcrumb_maker(station_view):
    def make(station):
        return [station.get_name(), reverse(station_view,
                                            kwargs={'station_id': station.station_id})
                ]
    return make


def make_order_breadcrumb_maker(station_order_view):
    def make(station_order):
        return ['Order #%s' % station_order.pk, reverse(station_order_view,
                                                        kwargs={'station_id': station_order.station.station_id,
                                                                'order_pk': station_order.pk})
                ]
    return make


def make_vehicle_breadcrumb_maker():
    def make(vehicle):
        return [vehicle.name, '']
    return make
