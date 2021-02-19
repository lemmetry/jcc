from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from fleet.models import Station
from jcc.make_breadcrumbs import make_home_breadcrumb


def user_sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    template = 'user_sign_in.html'
    return render(request, template, {})


def user_sign_out(request):
    logout(request)
    return redirect('user sign in')


@login_required
def home(request):
    stations = Station.objects.all()
    user = request.user

    breadcrumbs = [
        make_home_breadcrumb('home')
    ]

    template = 'home.html'
    context = {
        'stations': stations,
        'user': user,
        'breadcrumbs': breadcrumbs
    }

    return render(request, template, context)
