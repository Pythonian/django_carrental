from django.contrib import admin

from .models import Vehicle, Rent, Area

admin.site.register(Area)
admin.site.register(Vehicle)
admin.site.register(Rent)