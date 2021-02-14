from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signin', views.user_sign_in, name='user sign in'),
    path('signout', views.user_sign_out, name='user sign out'),
    path('stations', views.home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
