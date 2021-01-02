from django.shortcuts import render

from fleet.models import Vehicle
from inventory.models import BagCompartmentToItemAssociation
from inventory.models import KitToItemAssociation
from inventory.models import KitCompartmentToItemAssociation


def order_form(request):
    vehicle = Vehicle.objects.get(call_sign='M11')
    vehicle_to_bag_associations = vehicle.vehicletobagassociation_set.all()
    vehicle_bags = [vehicle_to_bag_association.bag for vehicle_to_bag_association in vehicle_to_bag_associations]

    r = request.GET
    for key, value in r.items():
        try:
            value = int(value)
            if value > 0:
                association_class_name = key.split('_')[0]
                association_object_pk = key.split('_')[1]
                # ^^^ association_class_name and association_pk will provide enough information about the ordered
                # item, including it's location.

                if association_class_name == 'bagcompartmenttoitemassociation':
                    bag_compartment_to_item_association = BagCompartmentToItemAssociation.objects.get(pk=association_object_pk)
                    item = bag_compartment_to_item_association.item
                    print('%s in %s' % (item.name, bag_compartment_to_item_association.bag_compartment.name))
                elif association_class_name == 'kittoitemassociation':
                    kit_to_item_association = KitToItemAssociation.objects.get(pk=association_object_pk)
                    item = kit_to_item_association.item
                    print('%s in %s' % (item.name, kit_to_item_association.kit.name))
                elif association_class_name == 'kitcompartmenttoitemassociation':
                    kit_compartment_to_item_association = KitCompartmentToItemAssociation.objects.get(pk=association_object_pk)
                    item = kit_compartment_to_item_association.item
                    print('%s in %s' % (item.name, kit_compartment_to_item_association.kit_compartment.name))
                else:
                    print('How did you get here?')

        except ValueError:
            pass

    template = 'order-form.html'
    context = {
        'vehicle_bags': vehicle_bags,
    }
    return render(request, template, context)
