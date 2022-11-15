# from django.test import TestCase
#
# from inventory.models import Bag, BagCompartment, Item, Kit
#
#
# class DummyTestCase(TestCase):
#     def setUp(self):
#         item_one = Item.objects.create(name='ItemOne')
#         item_two = Item.objects.create(name='ItemTwo')
#
#         kit_one = Kit.objects.create(name='KitOne')
#         kit_one.items.add(item_one, through_defaults={'quantity': 2, 'ordering': 3})
#
#         kit_two = Kit.objects.create(name='KitTwo')
#         kit_two.items.add(item_one, through_defaults={'quantity': 4, 'ordering': 5})
#         kit_two.items.add(item_two, through_defaults={'quantity': 6, 'ordering': 7})
#
#         compartment_one = BagCompartment.objects.create(name='CompartmentOne')
#         compartment_one.items.add(item_one, through_defaults={'quantity': 8, 'ordering': 9})
#         compartment_one.kits.add(kit_one, through_defaults={'ordering': 10})
#         compartment_one.kits.add(kit_two, through_defaults={'ordering': 11})
#
#         compartment_two = BagCompartment.objects.create(name='CompartmentTwo')
#         compartment_two.items.add(item_two, through_defaults={'quantity': 12, 'ordering': 13})
#
#         bag_one = Bag.objects.create(name='BagOne')
#         bag_one.compartments.add(compartment_one, through_defaults={'ordering': 14})
#         bag_one.compartments.add(compartment_two, through_defaults={'ordering': 15})
#
#     def test_it_works(self):
#         bags = Bag.objects.all()
#         for bag in bags:
#             print(f'Bag name={bag.name}')
#             for bag_compartment in bag.bagcompartmentassociation_set.all():
#                 print(f'  Compartment name={bag_compartment.compartment.name} ordering={bag_compartment.ordering}')
#                 for comparment_item in bag_compartment.compartment.compartmentitemassociation_set.all():
#                     print(f'    Item name={comparment_item.item.name} quantity={comparment_item.quantity} '
#                           f'ordering={comparment_item.ordering}')
#                 for compartment_kit in bag_compartment.compartment.compartmentkitassociation_set.all():
#                     print(f'    Kit name={compartment_kit.kit.name} ordering={compartment_kit.ordering}')
#                     for kit_item in compartment_kit.kit.kititemassociation_set.all():
#                         print(f'      Item name={kit_item.item.name} quantity={kit_item.quantity} '
#                               f'ordering={kit_item.ordering}')
