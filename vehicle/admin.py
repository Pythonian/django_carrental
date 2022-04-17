from django.contrib import admin

from .models import Vehicle, Rent, Area, CarType, GearType, FuelType


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'vendor', 'area', 'price', 'is_available']

admin.site.register(Area)
admin.site.register(Rent)
admin.site.register(CarType)
admin.site.register(GearType)
admin.site.register(FuelType)
