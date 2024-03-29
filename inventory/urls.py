from django.urls import path
from inventory import views as inventory_views

urlpatterns = [
    path('stations/<int:station_pk>/orders', inventory_views.station_orders_dashboard,
         name='station orders dashboard'),

    path('orders/<int:order_pk>', inventory_views.make_station_order,
         name='make station order'),

    path('orders/<int:order_pk>/fleet/<str:vehicle_path>', inventory_views.make_vehicle_order,
         name='make vehicle order'),

    path('orders/<int:order_pk>/confirmation', inventory_views.station_order_confirmation,
         name='station order confirmation'),

    path('orders/<int:order_pk>/summary', inventory_views.station_order_summary,
         name='station order summary'),
]
