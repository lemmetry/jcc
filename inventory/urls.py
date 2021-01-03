from django.urls import path
from . import views

urlpatterns = [
    path('order-form/<str:vehicle_call_sign>', views.order_form, name='order-form')
]
