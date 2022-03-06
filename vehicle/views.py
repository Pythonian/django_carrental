from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from account.models import VendorProfile
from .models import Vehicle, Rent
from .forms import VehicleForm, RentForm


def vendor_list(request):
    vendors = VendorProfile.objects.all()
    return render(
        request, 'vehicle/vendors.html',
        {'vendors': vendors})


def vehicle_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)

    return render(
        request, 'vehicle/list.html', {'vehicles': vehicles})


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    compared = bool
    if vehicle.compares.filter(id=request.user.id).exists():
        compared = True

    return render(
        request, 'vehicle/detail.html', {'vehicle': vehicle,
                                         'compared': compared})


def rented_vehicles(request):
    vehicles = Rent.objects.filter(customer=request.user)

    return render(
        request, 'rented_vehicles.html', {'vehicles': vehicles})


@login_required
def add_to_compare(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    if vehicle.compares.filter(id=request.user.id).exists():
        vehicle.compares.remove(request.user)
    else:
        vehicle.compares.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def compare_vehicles(request):
    vehicles = Vehicle.objects.filter(
        is_available=True).filter(compares=request.user)[:3]
    return render(
        request, 'vehicle/compare.html', {'vehicles': vehicles})


@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.vendor = request.user
            vehicle.save()
            messages.success(
                request, "Vehicle data successfully uploaded.")
            return redirect('vehicle:detail', vehicle.id)
        else:
            messages.warning(
                request, "An error occured, please check below.")
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
            messages.success(
                request, "Vehicle data successfully updated.")
            return redirect('vehicle:detail', vehicle.id)
        else:
            messages.warning(
                request, "An error occured, please check below.")
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


def check_availability(request, license_plate):
    import datetime

    date_of_booking = request.POST.get(
        'date_of_booking', '')
    date_of_return = request.POST.get(
        'date_of_return', '')

    date_of_booking = datetime.strptime(
        date_of_booking, '%Y-%m-%d').date()
    date_of_return = datetime.strptime(
        date_of_return, '%Y-%m-%d').date()

    rentvehicle = Rent.objects.filter(
        license_plate=license_plate)
    vehicle = Vehicle.objects.get(
        license_plate=license_plate)

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(
        customer_email=customer_email)

    if date_of_booking < datetime.date.today():
        Incorrect_dates = "Please give proper dates"
        return render(
            request, 'showdetails.html',
            {'Incorrect_dates': Incorrect_dates,
             'vehicle': vehicle, 'customer': customer})

    if date_of_return < date_of_booking:
        Incorrect_dates = "Please give proper dates"
        return render(
            request, 'showdetails_loggedin.html',
            {'Incorrect_dates': Incorrect_dates,
             'vehicle': vehicle, 'customer': customer})

    days = (date_of_return - date_of_booking).days + 1
    total = days * vehicle.price

    rent_data = {
        "date_of_booking": date_of_booking,
        "date_of_return": date_of_return,
        "days": days, "total": total
    }

    for rv in rentvehicle:
        if (rv.date_of_booking >= date_of_booking and date_of_return >= rv.date_of_booking) or (date_of_booking >= rv.date_of_booking and date_of_return <= rv.date_of_return) or (date_of_booking <= rv.date_of_return and date_of_return >= rv.date_of_return):
            if rv.isAvailable:
                Available = True
                Message = "Someone has requested for this vehicle from " + \
                    str(rv.RentVehicle_Date_of_Booking) + \
                    " to " + str(rv.RentVehicle_Date_of_Return)
                return render(
                    request,
                    'showdetails.html',
                    {'Message': Message,
                     'Available': Available,
                     'vehicle': vehicle,
                     'customer': customer,
                     'rent_data': rent_data})

            NotAvailable = True
            return render(
                request,
                'showdetails.html',
                {'NotAvailable': NotAvailable,
                 'dates': rv,
                 'vehicle': vehicle,
                 'customer': customer})

        # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
        #     Available = True
        #     return render(request,'showdetails_loggedin.html',{'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})

    Available = True

    return render(
        request, 'showdetails.html',
        {'Available': Available, 'vehicle': vehicle,
         'customer': customer, 'rent_data': rent_data})
