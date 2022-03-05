from django.shortcuts import render
from account.models import VendorProfile
from vehicle.models import Vehicle


def home(request):
    vehicles = Vehicle.objects.filter(is_available=True)[:3]
    vendors = VendorProfile.objects.all()
    return render(
        request, 'home.html',
        {'vehicles': vehicles, 'vendors': vendors})
