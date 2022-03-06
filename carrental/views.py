from django.shortcuts import render
from account.models import VendorProfile
from vehicle.models import Vehicle


def is_valid_query_paramter(param):
    return param != '' and param is not None


def home(request):
    vehicles = Vehicle.objects.filter(is_available=True)[:3]
    vendors = VendorProfile.objects.all()

    return render(
        request, 'home.html',
        {'vehicles': vehicles, 'vendors': vendors})


def search(request):
    qs = Vehicle.objects.all()

    car_name_query = request.GET.get('car_name')
    min_price_query = request.GET.get('min_price')
    max_price_query = request.GET.get('max_price')
    # search by Area?
    gear_type_query = request.GET.get('gear_type')
    car_type_query = request.GET.get('car_type')
    fuel_type_query = request.GET.get('fuel_type')

    if is_valid_query_paramter(car_name_query):
        qs = qs.filter(name__icontains=car_name_query)

    if is_valid_query_paramter(min_price_query):
        qs = qs.filter(price__gte=min_price_query)

    if is_valid_query_paramter(max_price_query):
        qs = qs.filter(price__lte=max_price_query)

    if is_valid_query_paramter(gear_type_query) and gear_type_query != '--Gear Type--':
        qs = qs.filter(gear_type__icontains=gear_type_query)

    if is_valid_query_paramter(car_type_query) and car_type_query != '--Car Type--':
        qs = qs.filter(car_type__icontains=car_type_query)

    if is_valid_query_paramter(fuel_type_query) and fuel_type_query != '--Fuel Type--':
        qs = qs.filter(fuel_type__icontains=fuel_type_query)

    context = {
        'vehicles': qs
    }

    return render(
        request, 'search.html', context)
