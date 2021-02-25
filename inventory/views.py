from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from fleet.models import Station, Vehicle
from inventory.models import StationOrder, VehicleOrder, BagCompartmentToItemAssociation, KitToItemAssociation, \
    KitCompartmentToItemAssociation, VehicleOrderToItemAssociation
from jcc.make_breadcrumbs import make_home_breadcrumb, make_station_breadcrumb, make_order_breadcrumb, \
    make_vehicle_breadcrumb
from jcc.settings.base import JCC_EMAIL_FROM, JCC_EMAIL_TO


@login_required
def station_orders_dashboard(request, station_id):
    station = Station.objects.get(station_id=station_id)

    if request.method == 'POST':
        new_station_order = StationOrder.objects.create(station=station)
        order_pk = new_station_order.pk
        return redirect('make station order', station_id, order_pk)

    else:
        station_name = station.get_name()
        last_five_station_orders = station.stationorder_set.all().order_by('-pk')[:5][::-1]
        if last_five_station_orders:
            last_five_station_orders = reversed(last_five_station_orders)

    breadcrumbs = [
        make_home_breadcrumb(),
        make_station_breadcrumb(station)
    ]

    template = 'station_orders_dashboard.html'
    context = {
        'station_id': station_id,
        'station_name': station_name,
        'last_five_station_orders': last_five_station_orders,
        'breadcrumbs': breadcrumbs
    }
    return render(request, template, context)


@login_required
def make_station_order(request, station_id, order_pk):
    station = Station.objects.all().filter(station_id=station_id)[0]
    station_name = station.get_name()
    station_fleet = Vehicle.objects.filter(station=station_id)
    station_order = StationOrder.objects.get(pk=order_pk)

    items_of_station_order_grouped_by_vehicle_then_bag = station_order.get_items_grouped_by_vehicle_then_bag()

    breadcrumbs = [
        make_home_breadcrumb(),
        make_station_breadcrumb(station),
        make_order_breadcrumb(station_order)
    ]

    template = 'make_station_order.html'
    context = {
        'station_id': station_id,
        'order_pk': order_pk,
        'station_name': station_name,
        'station_fleet': station_fleet,
        'items_of_station_order_grouped_by_vehicle_then_bag': items_of_station_order_grouped_by_vehicle_then_bag,
        'breadcrumbs': breadcrumbs
    }
    return render(request, template, context)


@login_required
def make_vehicle_order(request, station_id, order_pk, vehicle_path):
    station = Station.objects.get(station_id=station_id)
    station_name = station.get_name()
    station_order = StationOrder.objects.get(pk=order_pk)

    vehicle_name = vehicle_path.replace('_', ' ')
    vehicle_name = vehicle_name.capitalize()
    vehicle = Vehicle.objects.get(name=vehicle_name)

    vehicle_to_bag_associations = vehicle.vehicletobagassociation_set.all()
    vehicle_bags = [vehicle_to_bag_association.bag
                    for vehicle_to_bag_association in vehicle_to_bag_associations]

    if request.method == 'POST':
        r = request.POST
        vehicle_order = VehicleOrder.objects.create(vehicle=vehicle,
                                                    station_order=station_order)

        for key, value in r.items():
            try:
                value = int(value)
                if value > 0:
                    item_location_association_class_name = key.split('_')[0]
                    item_location_association_object_pk = key.split('_')[1]

                    if item_location_association_class_name == 'bagcompartmenttoitemassociation':
                        bag_compartment_to_item_association = \
                            BagCompartmentToItemAssociation.objects.get(pk=item_location_association_object_pk)
                        item = bag_compartment_to_item_association.item
                        bag = bag_compartment_to_item_association.bag_compartment.bag

                    elif item_location_association_class_name == 'kittoitemassociation':
                        kit_to_item_association = \
                            KitToItemAssociation.objects.get(pk=item_location_association_object_pk)
                        item = kit_to_item_association.item
                        bag = kit_to_item_association.kit.bag_compartment.bag

                    elif item_location_association_class_name == 'kitcompartmenttoitemassociation':
                        kit_compartment_to_item_association = \
                            KitCompartmentToItemAssociation.objects.get(pk=item_location_association_object_pk)
                        item = kit_compartment_to_item_association.item
                        bag = kit_compartment_to_item_association.kit_compartment.kit.bag_compartment.bag

                    else:
                        bag = None
                        item = None
                        print('How did you get here?')

                    item_quantity = value
                    vehicle_order_to_item_association = VehicleOrderToItemAssociation(vehicle_order=vehicle_order,
                                                                                      bag=bag,
                                                                                      item=item,
                                                                                      quantity=item_quantity)
                    vehicle_order_to_item_association.save()
            except ValueError:
                pass

        return redirect('make station order', station_id, order_pk)
    else:

        breadcrumbs = [
            make_home_breadcrumb(),
            make_station_breadcrumb(station),
            make_order_breadcrumb(station_order),
            make_vehicle_breadcrumb(vehicle)
        ]

        template = 'make_vehicle_order.html'
        new_column_cutoffs = ['ETT Side',
                              'Under Syringes',
                              'Left Outside Pocket',
                              'Top Outside Pouches',
                              'Top Outside Flap',
                              'Inside Bag Main']
        context = {
            'station_id': station_id,
            'order_pk': order_pk,
            'station_name': station_name,
            'vehicle_name': vehicle_name,
            'vehicle_bags': vehicle_bags,
            'new_column_cutoffs': new_column_cutoffs,
            'breadcrumbs': breadcrumbs
        }

    return render(request, template, context)


@login_required
def station_order_confirmation(request, station_id, order_pk):
    station = Station.objects.get(station_id=station_id)
    station_name = station.get_name()
    station_order = StationOrder.objects.get(pk=order_pk)

    items_of_station_order_grouped_by_vehicle_then_bag = station_order.get_items_grouped_by_vehicle_then_bag()
    items_of_station_order_summed_regardless_of_location = station_order.get_items_summed_regardless_of_location()

    if request.method == 'POST':
        station_order.is_submitted = True
        station_order.timestamp = timezone.now()
        station_order.save()

        station_order_timestamp = station_order.timestamp
        email_context = {
            'station_name': station_name,
            'order_pk': order_pk,
            'items_ordered': items_of_station_order_summed_regardless_of_location,
            'order_timestamp': station_order_timestamp
        }
        email_subject = render_to_string(template_name='email_subject.txt',
                                         context=email_context)
        email_body_plain = render_to_string(template_name='email_body.txt',
                                            context=email_context)
        email_body_in_html = render_to_string(template_name='email_body.html',
                                              context=email_context)
        email = EmailMultiAlternatives(subject=email_subject,
                                       from_email=JCC_EMAIL_FROM,
                                       to=[JCC_EMAIL_TO],
                                       body=email_body_plain)
        email.attach_alternative(email_body_in_html, 'text/html')
        email.send()

        return redirect('station order summary', station_id, order_pk)

    breadcrumbs = [
        make_home_breadcrumb(),
        make_station_breadcrumb(station),
        make_order_breadcrumb(station_order),
    ]

    template = 'station_order_confirmation.html'
    context = {
        'station_id': station_id,
        'order_pk': order_pk,
        'station_name': station_name,
        'items_of_station_order_grouped_by_vehicle_then_bag': items_of_station_order_grouped_by_vehicle_then_bag,
        'items_of_station_order_summed_regardless_of_location': items_of_station_order_summed_regardless_of_location,
        'breadcrumbs': breadcrumbs
    }
    return render(request, template, context)


@login_required
def station_order_summary(request, station_id, order_pk):
    station = Station.objects.get(station_id=station_id)
    station_name = station.get_name()
    station_order = StationOrder.objects.get(pk=order_pk)
    station_order_timestamp = station_order.timestamp

    items_of_station_order_grouped_by_vehicle_then_bag = station_order.get_items_grouped_by_vehicle_then_bag()
    items_of_station_order_summed_regardless_of_location = station_order.get_items_summed_regardless_of_location()

    breadcrumbs = [
        make_home_breadcrumb(),
        make_station_breadcrumb(station),
        make_order_breadcrumb(station_order),
    ]

    template = 'station_order_summary.html'
    context = {
        'station_id': station_id,
        'order_pk': order_pk,
        'station_name': station_name,
        'station_order_timestamp': station_order_timestamp,
        'items_of_station_order_grouped_by_vehicle_then_bag': items_of_station_order_grouped_by_vehicle_then_bag,
        'items_of_station_order_summed_regardless_of_location': items_of_station_order_summed_regardless_of_location,
        'breadcrumbs': breadcrumbs
    }
    return render(request, template, context)
