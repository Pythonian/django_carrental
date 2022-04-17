from django.shortcuts import render
from account.models import VendorProfile
from vehicle.models import Vehicle, GearType, CarType, FuelType, Area


def is_valid_query_paramter(param):
    return param != '' and param is not None


def home(request):
    vehicles = Vehicle.objects.filter(is_available=True)[:3]
    vendors = VendorProfile.objects.all()
    gear_types = GearType.objects.all()
    car_types = CarType.objects.all()
    fuel_types = FuelType.objects.all()
    areas = Area.objects.all()

    return render(
        request, 'home.html',
        {'vehicles': vehicles, 'vendors': vendors,
         'gear_types': gear_types, 'car_types': car_types,
         'fuel_types': fuel_types, 'areas': areas})


def search(request):
    qs = Vehicle.objects.all()
    gear_types = GearType.objects.all()
    car_types = CarType.objects.all()
    fuel_types = FuelType.objects.all()
    areas = Area.objects.all()

    car_name_query = request.GET.get('car_name')
    min_price_query = request.GET.get('min_price')
    max_price_query = request.GET.get('max_price')
    area_query = request.GET.get('area')
    gear_type_query = request.GET.get('gear_type')
    car_type_query = request.GET.get('car_type')
    fuel_type_query = request.GET.get('fuel_type')

    if is_valid_query_paramter(car_name_query):
        qs = qs.filter(name__icontains=car_name_query)

    if is_valid_query_paramter(min_price_query):
        qs = qs.filter(price__gte=min_price_query)

    if is_valid_query_paramter(max_price_query):
        qs = qs.filter(price__lte=max_price_query)

    if is_valid_query_paramter(area_query) and area_query != '--Area--':
        qs = qs.filter(area=area_query)

    if is_valid_query_paramter(gear_type_query) and gear_type_query != '--Gear Type--':
        qs = qs.filter(gear_type=gear_type_query)

    if is_valid_query_paramter(car_type_query) and car_type_query != '--Car Type--':
        qs = qs.filter(car_type=car_type_query)

    if is_valid_query_paramter(fuel_type_query) and fuel_type_query != '--Fuel Type--':
        qs = qs.filter(fuel_type=fuel_type_query)

    context = {
        'vehicles': qs,
        'gear_types': gear_types, 'car_types': car_types,
        'fuel_types': fuel_types, 'areas': areas
    }

    return render(
        request, 'search.html', context)
