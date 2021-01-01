from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import OrderForm
from inventory.models import Bag


def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = OrderForm()

        red_bag = Bag.objects.get(name='Red Bag "Stat Pack"')
        vehicle_bags = [red_bag]

        r = request.GET
        for key, value in r.items():
            try:
                value = int(value)
                if value > 0:
                    association_class_name = key.split('_')[0]
                    association_object_pk = key.split('_')[1]
                    # ^^^ association_class_name and association_pk will provide enough information about the ordered
                    # item, including it's location.
                    print('association_class_name: %s, '
                          'association_object_pk: %s' % (association_class_name, association_object_pk))
            except ValueError:
                pass

        template = 'order-form.html'
        context = {
            'form': form,
            'vehicle_bags': vehicle_bags,
        }
        return render(request, template, context)
