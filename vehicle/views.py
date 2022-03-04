from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Vehicle, Rent
from .forms import VehicleForm, RentForm


def vehicle_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)

    return render(
        request, 'vehicle/list.html', {'vehicles': vehicles})


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)

    return render(
        request, 'vehicle/detail.html', {'vehicle': vehicle})


def rented_vehicles(request):
    vehicles = Rent.objects.filter(customer=request.user)

    return render(
        request, 'rented_vehicles.html', {'vehicles': vehicles})


def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.vendor = request.user
            vehicle.save()
            return redirect('vehicle_detail')
    else:
        form = VehicleForm()

    return render(
        request, 'vehicle/form.html', {'form': form, 'create': True})


def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_detail')
    else:
        form = VehicleForm(instance=vehicle)

    return render(request,
                  'vehicle/form.html',
                  {'form': form, 'create': False, 'vehicle': vehicle})


def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle successfully deleted')
        return redirect('vehicle_list')

    return render(request,
                  'vehicle/confirm_delete.html',
                  {'vehicle': vehicle})


@login_required
def rent_vehicle(request):
    vehicle = get_object_or_404(Vehicle, id=id)
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.customer = request.user
            rent.vendor = request.user
            rent.vehicle = vehicle
            rent.save()
            return redirect('vehicle_detail', args=[vehicle.id])
    else:
        form = RentForm()
    return render(request, '', {})

    # RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')
    # RentVehicle_Date_of_Return=request.POST.get('RentVehicle_Date_of_Return','')
    # Total_days=request.POST.get('Total_days','')
    # RentVehicle_Total_amount=request.POST.get('RentVehicle_Total_amount','')
    # Vehicle_license_plate=request.POST.get('Vehicle_license_plate','')
    # RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')

    # RentVehicle_Date_of_Booking = datetime.strptime(
    #     RentVehicle_Date_of_Booking, '%b. %d, %Y').date()
    # RentVehicle_Date_of_Return = datetime.strptime(
    #     RentVehicle_Date_of_Return, '%b. %d, %Y').date()

    # rentvehicle = RentVehicle(
    #     RentVehicle_Date_of_Booking=RentVehicle_Date_of_Booking,
    #     RentVehicle_Date_of_Return=RentVehicle_Date_of_Return,
    #     Total_days=Total_days,RentVehicle_Total_amount=RentVehicle_Total_amount,
    #     Vehicle_license_plate=Vehicle_license_plate,customer_email=user_email)

    # rentvehicle.save()

    # customer = Customer.objects.filter(customer_email=user_email)
    # if customer.exists():
    #     return redirect("/SentRequests/")
