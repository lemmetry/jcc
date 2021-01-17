from django.urls import path
from fleet import views as fleet_views
from inventory import views as inventory_views

urlpatterns = [
    path('stations/<int:station_id>/orders', inventory_views.station_orders_dashboard,
         name='station_orders_dashboard'),

    path('stations/<int:station_id>/orders/<int:order_pk>', inventory_views.make_station_order,
         name='make station order'),

    path('stations/<int:station_id>/orders/<int:order_pk>/fleet/<str:vehicle_path>', inventory_views.make_vehicle_order,
         name='order form'),

    path('stations/<str:station_id>/orders/<str:order_pk>/confirmation', inventory_views.station_order_confirmation,
         name='station order confirmation'),
]
