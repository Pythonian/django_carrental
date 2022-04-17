from django.contrib import admin

from .models import Vehicle, Rent, Area, CarType, GearType, FuelType

admin.site.register(Area)
admin.site.register(Vehicle)
admin.site.register(Rent)
admin.site.register(CarType)
admin.site.register(GearType)
admin.site.register(FuelType)
