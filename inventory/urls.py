from django.urls import path
from fleet import views as fleet_views
from inventory import views as inventory_views

urlpatterns = [
    path('station_<str:station_id>/orders/', inventory_views.orders, name='orders'),
    path('station_<str:station_id>/fleet', fleet_views.station_fleet, name='station fleet'),
    path('order_form/<str:vehicle_call_sign>', inventory_views.order_form, name='order_form'),
    path('review_order/<str:vehicle_order_pk>', inventory_views.review_order, name='review_order')
]
