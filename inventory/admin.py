from django.contrib import admin
from .models import Bag
from .models import BagCompartment
from .models import BagCompartmentToItemAssociation
from .models import Kit
from .models import KitToItemAssociation
from .models import KitCompartment
from .models import KitCompartmentToItemAssociation
from .models import Item
from .models import VehicleOrder
from .models import VehicleOrderToItemAssociation


class BagCompartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_bag_name')


class BagCompartmentToItemAssociationAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'bag_compartment')


class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_bag_name', 'get_bag_compartment_name')


class KitToItemAssociationAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'kit')


class KitCompartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_kit_name', 'get_items')

    def get_items(self, obj):
        try:
            return ";\n ".join([i.name + " (" + i.size + ")" for i in obj.items.all()])
        except AttributeError:
            return 'Empty Kit Compartment'
    get_items.short_description = 'Items'


class VehicleOrderToItemAssociationAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')


admin.site.register(Bag)
admin.site.register(BagCompartment, BagCompartmentAdmin)
admin.site.register(BagCompartmentToItemAssociation, BagCompartmentToItemAssociationAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(KitToItemAssociation, KitToItemAssociationAdmin)
admin.site.register(KitCompartment, KitCompartmentAdmin)
admin.site.register(KitCompartmentToItemAssociation)
admin.site.register(Item)
admin.site.register(VehicleOrder)
admin.site.register(VehicleOrderToItemAssociation, VehicleOrderToItemAssociationAdmin)
