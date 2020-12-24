from django.contrib import admin
from .models import Bag
from .models import BagCompartment
from .models import Kit
from .models import KitCompartment
from .models import Item


class BagCompartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_bag_name')


class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_bag_name', 'get_bag_compartment_name')


class KitCompartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_kit_name', 'get_items')

    def get_items(self, obj):
        return ";\n ".join([i.name + " (" + i.size + ")" for i in obj.items.all()])


admin.site.register(Bag)
admin.site.register(BagCompartment, BagCompartmentAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(KitCompartment, KitCompartmentAdmin)
admin.site.register(Item)
