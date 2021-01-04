from django.urls import path
from . import views

urlpatterns = [
    path('station_<str:station_id>/recent_orders/', views.recent_orders, name='recent_orders'),
    path('order_form/<str:vehicle_call_sign>', views.order_form, name='order_form'),
    path('review_order/<str:vehicle_order_pk>', views.review_order, name='review_order')
]
