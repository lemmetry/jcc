from django.test import TestCase

from inventory.models import Bag, Compartment, Item, Kit


class DummyTestCase(TestCase):
    def setUp(self):
        itemOne = Item.objects.create(name='ItemOne')
        itemTwo = Item.objects.create(name='ItemTwo')

        kitOne = Kit.objects.create(name='KitOne')
        kitOne.items.add(itemOne, through_defaults={'quantity': 2, 'ordering': 3})

        kitTwo = Kit.objects.create(name='KitTwo')
        kitTwo.items.add(itemOne, through_defaults={'quantity': 4, 'ordering': 5})
        kitTwo.items.add(itemTwo, through_defaults={'quantity': 6, 'ordering': 7})

        compartmentOne = Compartment.objects.create(name='CompartmentOne')
        compartmentOne.items.add(itemOne, through_defaults={'quantity': 8, 'ordering': 9})
        compartmentOne.kits.add(kitOne, through_defaults={'ordering': 10})
        compartmentOne.kits.add(kitTwo, through_defaults={'ordering': 11})

        compartmentTwo = Compartment.objects.create(name='CompartmentTwo')
        compartmentTwo.items.add(itemTwo, through_defaults={'quantity': 12, 'ordering': 13})

        bagOne = Bag.objects.create(name='BagOne')
        bagOne.compartments.add(compartmentOne, through_defaults={'ordering': 14})
        bagOne.compartments.add(compartmentTwo, through_defaults={'ordering': 15})

    def test_it_works(self):
        bags = Bag.objects.all()
        for bag in bags:
            print(f'Bag name={bag.name}')
            for bagCompartment in bag.bagcompartmentassociation_set.all():
                print(f'  Compartment name={bagCompartment.compartment.name} ordering={bagCompartment.ordering}')
                for comparmentItem in bagCompartment.compartment.compartmentitemassociation_set.all():
                    print(f'    Item name={comparmentItem.item.name} quantity={comparmentItem.quantity} '
                          f'ordering={comparmentItem.ordering}')
                for compartmentKit in bagCompartment.compartment.compartmentkitassociation_set.all():
                    print(f'    Kit name={compartmentKit.kit.name} ordering={compartmentKit.ordering}')
                    for kitItem in compartmentKit.kit.kititemassociation_set.all():
                        print(f'      Item name={kitItem.item.name} quantity={kitItem.quantity} '
                              f'ordering={kitItem.ordering}')
