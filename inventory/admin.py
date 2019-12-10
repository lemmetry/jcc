from django.contrib import admin
from .models import Item
from .models import Compartment
from .models import CompartmentItemAssociation
from .models import CompartmentKitAssociation
from .models import Bag
from .models import BagCompartmentAssociation
from .models import Kit
from .models import KitItemAssociation
from .models import KitCompartmentAssociation


class CompartmentItemAssociationAdmin(admin.ModelAdmin):
    list_display = ('item', 'compartment')


class CompartmentKitAssociationAdmin(admin.ModelAdmin):
    list_display = ('kit', 'compartment')

    def get_bag_name(self, obj):
        pass
        # TODO add bag_name field for easy sorting


class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_items')

    def get_items(self, obj):
        return ";\n ".join([i.name + " (" + i.size + ")" for i in obj.items.all()])


class KitItemAssociationAdmin(admin.ModelAdmin):
    list_display = ('item', 'kit')


class KitCompartmentAssociationAdmin(admin.ModelAdmin):
    list_display = ('compartment', 'kit')


class BagCompartmentAssociationAdmin(admin.ModelAdmin):
    list_display = ('compartment', 'bag')


admin.site.register(Item)
admin.site.register(Compartment)
admin.site.register(CompartmentItemAssociation, CompartmentItemAssociationAdmin)
admin.site.register(CompartmentKitAssociation, CompartmentKitAssociationAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(KitItemAssociation, KitItemAssociationAdmin)
admin.site.register(KitCompartmentAssociation, KitCompartmentAssociationAdmin)
admin.site.register(Bag)
admin.site.register(BagCompartmentAssociation, BagCompartmentAssociationAdmin)
