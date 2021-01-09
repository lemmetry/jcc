from django.shortcuts import render
from django.shortcuts import redirect

from fleet.models import Station
from fleet.models import Vehicle
from inventory.models import BagCompartmentToItemAssociation
from inventory.models import KitToItemAssociation
from inventory.models import KitCompartmentToItemAssociation
from inventory.models import VehicleOrder
from inventory.models import VehicleOrderToItemAssociation
from inventory.models import StationOrder


def orders(request, station_id):
    station = Station.objects.get(station_id=station_id)
    station_name = station.get_name()
    last_five_station_orders = station.stationorder_set.all()[:5]
    if last_five_station_orders:
        last_five_station_orders = reversed(last_five_station_orders)
        no_records_exist_message = None
    else:
        no_records_exist_message = "No Orders Found."

    template = 'orders.html'
    context = {
        'station_id': station_id,
        'station_name': station_name,
        'last_five_station_orders': last_five_station_orders,
        'no_records_exist_message': no_records_exist_message
    }
    return render(request, template, context)


def order_form(request, station_id, vehicle_path):
    station = Station.objects.get(station_id=station_id)
    station_name = station.get_name()

    vehicle_name = vehicle_path.replace('_', ' ')  # TODO I don't like this part.
    vehicle_name = vehicle_name.capitalize()       # TODO Create vehicle_id field instead?
    vehicle = Vehicle.objects.get(name=vehicle_name)

    vehicle_to_bag_associations = vehicle.vehicletobagassociation_set.all()
    vehicle_bags = [vehicle_to_bag_association.bag for vehicle_to_bag_association in vehicle_to_bag_associations]

    if request.method == 'POST':
        r = request.POST
        vehicle_order = VehicleOrder.objects.create(vehicle=vehicle)

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

        return redirect('station fleet', station_id)
    else:
        template = 'order_form.html'
        new_column_cutoffs = ['ETT Side',
                              'Under Syringes',
                              'Left Outside Pocket',
                              'Top Outside Pouches',
                              'Top Outside Flap',
                              'Inside Bag Main']
        context = {
            'station_id': station_id,
            'station_name': station_name,
            'vehicle_name': vehicle_name,
            'vehicle_bags': vehicle_bags,
            'new_column_cutoffs': new_column_cutoffs
        }

    return render(request, template, context)


def review_order(request, vehicle_order_pk):
    vehicle_order = VehicleOrder.objects.get(pk=vehicle_order_pk)
    vehicle_name = vehicle_order.vehicle.name
    vehicle_order_to_item_associations = vehicle_order.vehicleordertoitemassociation_set.all()

    template = 'review_order.html'
    context = {
        'vehicle_order': vehicle_order,
        'vehicle_name': vehicle_name,
        'vehicle_order_to_item_associations': vehicle_order_to_item_associations
    }
    return render(request, template, context)


def order_details(request, station_id, order_pk):
    station_order = StationOrder.objects.get(pk=order_pk)
    vehicle_orders = station_order.vehicleorder_set.all()

    template = 'order_details.html'
    context = {
        'station_id': station_id,
        'order_pk': order_pk,
        'vehicle_orders': vehicle_orders
    }
    return render(request, template, context)


def order_confirmation(request, station_id, order_pk):
    vehicle_order = VehicleOrder.objects.get(pk=order_pk)
    orders = vehicle_order.vehicleordertoitemassociation_set.all()

    template = 'order_confirmation.html'
    context = {
        'orders': orders
    }
    return render(request, template, context)
