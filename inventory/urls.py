from django.urls import path
from fleet import views as fleet_views
from inventory import views as inventory_views

urlpatterns = [
    path('station_<str:station_id>/orders/',
         inventory_views.orders, name='orders'),
    path('station_<str:station_id>/fleet',
         fleet_views.station_fleet, name='station fleet'),
    path('station_<str:station_id>/<str:vehicle_path>',
         inventory_views.order_form, name='order_form'),
    path('station_<str:station_id>/order_<str:order_pk>/confirmation',
         inventory_views.order_confirmation, name='order confirmation'),
    path('review_order/<str:vehicle_order_pk>',
         inventory_views.review_order, name='review_order')
]
