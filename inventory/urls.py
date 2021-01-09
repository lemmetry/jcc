from django.urls import path
from fleet import views as fleet_views
from inventory import views as inventory_views

urlpatterns = [
    path('stations/<str:station_id>/orders', inventory_views.orders,
         name='orders'),

    path('stations/<str:station_id>/fleet', fleet_views.station_fleet,
         name='station fleet'),

    path('stations/<str:station_id>/fleet/<str:vehicle_path>', inventory_views.order_form,
         name='order form'),

    path('stations/<str:station_id>/orders/<str:order_pk>/confirmation', inventory_views.order_confirmation,
         name='order confirmation'),
]
