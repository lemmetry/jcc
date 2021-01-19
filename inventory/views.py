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
            no_records_exist_message = None
        else:
            no_records_exist_message = "No Orders Found."

    template = 'station_orders_dashboard.html'
    context = {
        'station_id': station_id,
        'station_name': station_name,
        'last_five_station_orders': last_five_station_orders,
        'no_records_exist_message': no_records_exist_message
    }
    return render(request, template, context)


def make_station_order(request, station_id, order_pk):
    station = Station.objects.all().filter(station_id=station_id)[0]
    station_name = station.get_name()
    station_fleet = Vehicle.objects.filter(station=station_id)
    station_order = StationOrder.objects.get(pk=order_pk)

    # get ALL VehicleOrder-s associated with StationOrder
    vehicle_orders = station_order.vehicleorder_set.all().order_by('-vehicle')
    print('\nvehicle_orders:\n  %s' % vehicle_orders)

    # get ALL VehicleOrderToItemAssociation-s associated with ALL VehicleOrder-s from above
    vehicle_order_to_item_associations = [
        vehicle_order_to_item_association
        for vehicle_order in vehicle_orders
        for vehicle_order_to_item_association in vehicle_order.vehicleordertoitemassociation_set.all()
    ]
    print('\nvehicle_order_to_item_associations:\n  %s\n' % vehicle_order_to_item_associations)

    votia_grouped = {} # vehicle_order_to_item_association
    for vehicle_order_to_item_association in vehicle_order_to_item_associations:
        vehicle_name = vehicle_order_to_item_association.vehicle_order.vehicle.name
        if vehicle_name not in votia_grouped.keys():
            votia_grouped[vehicle_name] = {}

        bag_name = vehicle_order_to_item_association.bag.name
        if bag_name not in votia_grouped[vehicle_name].keys():
            votia_grouped[vehicle_name][bag_name] = {}

        item_name = vehicle_order_to_item_association.item.name
        if item_name not in votia_grouped[vehicle_name][bag_name].keys():
            votia_grouped[vehicle_name][bag_name][item_name] = 0

        item_quantity = vehicle_order_to_item_association.quantity
        votia_grouped[vehicle_name][bag_name][item_name] += item_quantity
    print('\ngrouped_by_vehicle: ', votia_grouped)

    if request.method == 'POST':
        station_order.is_submitted = True
        station_order.save()
        return redirect('station order confirmation', station_id, order_pk)

    vehicle_description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ' \
                          'ut labore et dolore magna aliqua.'
    dummy_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut ' \
                 'labore et dolore magna aliqua.'

    template = 'make_station_order.html'
    context = {
        'station_id': station_id,
        'order_pk': order_pk,
        'station_name': station_name,
        'station_fleet': station_fleet,
        'station_order': station_order,
        'vehicle_orders': vehicle_orders,
        'img_src': 'https://via.placeholder.com/150x100.png',
        'vehicle_description': vehicle_description,
        'dummy_text': dummy_text
    }
    return render(request, template, context)


def make_vehicle_order(request, station_id, order_pk, vehicle_path):
    station = Station.objects.get(station_id=station_id)
    station_name = station.get_name()
    station_order = StationOrder.objects.get(pk=order_pk)

    vehicle_name = vehicle_path.replace('_', ' ')  # TODO I don't like this part.
    vehicle_name = vehicle_name.capitalize()       # TODO Create vehicle_id field instead?
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
            'new_column_cutoffs': new_column_cutoffs
        }

    return render(request, template, context)


def station_order_confirmation(request, station_id, order_pk):
    station_order = StationOrder.objects.get(pk=order_pk)
    vehicle_orders = station_order.vehicleorder_set.all()

    template = 'station_order_confirmation.html'
    context = {
        'vehicle_orders': vehicle_orders
    }
    return render(request, template, context)
