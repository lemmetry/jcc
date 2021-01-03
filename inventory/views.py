from django.shortcuts import render
from django.http import HttpResponseRedirect

from fleet.models import Vehicle
from inventory.models import BagCompartmentToItemAssociation
from inventory.models import KitToItemAssociation
from inventory.models import KitCompartmentToItemAssociation
from inventory.models import BagOrderToItemAssociation


def order_form(request):
    vehicle = Vehicle.objects.get(call_sign='M11')
    vehicle_to_bag_associations = vehicle.vehicletobagassociation_set.all()
    vehicle_bags = [vehicle_to_bag_association.bag for vehicle_to_bag_association in vehicle_to_bag_associations]

    if request.method == 'POST':
        r = request.POST
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
                        # print('%s in %s' % (item.name, bag_compartment_to_item_association.bag_compartment.name))
                    elif item_location_association_class_name == 'kittoitemassociation':
                        kit_to_item_association = \
                            KitToItemAssociation.objects.get(pk=item_location_association_object_pk)
                        item = kit_to_item_association.item
                        # print('%s in %s' % (item.name, kit_to_item_association.kit.name))
                    elif item_location_association_class_name == 'kitcompartmenttoitemassociation':
                        kit_compartment_to_item_association = \
                            KitCompartmentToItemAssociation.objects.get(pk=item_location_association_object_pk)
                        item = kit_compartment_to_item_association.item
                        # print('%s in %s' % (item.name, kit_compartment_to_item_association.kit_compartment.name))
                    else:
                        item = None
                        print('How did you get here?')

                    item_quantity = value
                    # print('%s - pk: %s;  %s x%s' % (item_location_association_class_name,
                    #                                 item_location_association_object_pk,
                    #                                 item,
                    #                                 item_quantity))
                    bag_order_to_item_association = BagOrderToItemAssociation(item=item, quantity=item_quantity)
                    bag_order_to_item_association.save()
            except ValueError:
                pass

        return HttpResponseRedirect('order-form')
    else:
        pass

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

