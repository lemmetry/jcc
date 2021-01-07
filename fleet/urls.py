from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('station_<str:station_id>/<str:vehicle_path>', views.vehicle, name='vehicle #')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
