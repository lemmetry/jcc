from django.contrib import admin
from .models import Item
from .models import Compartment
from .models import Kit
from .models import Bag


class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_items')

    def get_items(self, obj):
        return ";\n ".join([i.name + " (" + i.size + ")" for i in obj.items.all()])


admin.site.register(Item)
admin.site.register(Compartment)
admin.site.register(Kit, KitAdmin)
admin.site.register(Bag)
