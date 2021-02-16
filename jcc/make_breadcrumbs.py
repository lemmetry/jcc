from django.urls import reverse
from fleet import views as fleet_views
from inventory import views as inventory_views


def make_home_breadcrumb():
    return ['Home', reverse(fleet_views.home)]


def make_station_breadcrumb(station):
    breadcrumb_station_url = reverse(inventory_views.station_orders_dashboard,
                                     kwargs={'station_id': station.station_id}
                                     )
    return [station.get_name(), breadcrumb_station_url]


def make_order_breadcrumbs(station_order):
    breadcrumb_order_url = reverse(inventory_views.make_station_order,
                                   kwargs={'station_id': station_order.station.station_id,
                                           'order_pk': station_order.pk}
                                   )
    return ['Order #%s' % station_order.pk, breadcrumb_order_url]


def make_vehicle_breadcrumb(vehicle):
    return [vehicle.name, '']
