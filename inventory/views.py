from django.shortcuts import render
from django.shortcuts import redirect

from fleet.models import Vehicle
from inventory.models import BagCompartmentToItemAssociation
from inventory.models import KitToItemAssociation
from inventory.models import KitCompartmentToItemAssociation
from inventory.models import VehicleOrder
from inventory.models import VehicleOrderToItemAssociation


def order_form(request, vehicle_call_sign):
    vehicle = Vehicle.objects.get(call_sign=vehicle_call_sign)
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

        return redirect('order-form', vehicle_call_sign=vehicle_call_sign)
    else:
        template = 'order-form.html'
        new_column_cutoffs = ['ETT Side',
                              'Under Syringes',
                              'Left Outside Pocket',
                              'Top Outside Pouches',
                              'Top Outside Flap',
                              'Inside Bag Main']
        context = {
            'vehicle_bags': vehicle_bags,
            'new_column_cutoffs': new_column_cutoffs
        }

    return render(request, template, context)
