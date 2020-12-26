from django.contrib import admin
from .models import Station
from .models import Vehicle
from .models import VehicleBagAssociation


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'station')


class VehicleBagAssociationAdmin(admin.ModelAdmin):
    list_display = ('bag', 'quantity', 'vehicle')


admin.site.register(Station)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleBagAssociation, VehicleBagAssociationAdmin)
