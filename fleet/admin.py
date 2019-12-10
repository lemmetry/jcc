from django.contrib import admin
from .models import Station
from .models import Vehicle
from .models import VehicleBagAssociation


class VehicleBagAssociationAdmin(admin.ModelAdmin):
    list_display = ('bag', 'vehicle')


admin.site.register(Station)
admin.site.register(Vehicle)
admin.site.register(VehicleBagAssociation, VehicleBagAssociationAdmin)
