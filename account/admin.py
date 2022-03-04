from django.contrib import admin

from .models import User, VendorProfile, CustomerProfile

admin.site.register(User)
admin.site.register(VendorProfile)
admin.site.register(CustomerProfile)
