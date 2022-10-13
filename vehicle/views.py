from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.conf import settings

from carrental.utils import mk_paginator
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
    vehicles = mk_paginator(request, vehicles, 9)

    return render(
        request, 'vehicle/list.html', {'vehicles': vehicles})


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    recommended_vehicles = Vehicle.objects.exclude(id=vehicle.id).order_by('?')[:3]
    compared = bool
    if vehicle.compares.filter(id=request.user.id).exists():
        compared = True
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.customer = request.user
            rent.vehicle = vehicle
            rent.vendor = vehicle.vendor.vendor_profile
            rent.save()
            request.session['order_id'] = rent.id
            return redirect('vehicle:confirm_booking')
        else:
            messages.warning(
                request, "Your selected dates are incorrect. Try again")
    else:
        form = RentForm()

    return render(
        request, 'vehicle/detail.html', {'vehicle': vehicle,
                                         'recommended_vehicles': recommended_vehicles,
                                         'compared': compared,
                                         'form': form})


@login_required
def confirm_booking(request):
    rent_id = request.session.get('order_id')
    rent = get_object_or_404(Rent, id=rent_id)

    paystack_amount = int(rent.get_total_cost * 100)
    paystack_ref = None
    if not paystack_ref:
        paystack_ref = get_random_string(length=12).upper()
        rent.paystack_id = paystack_ref
        rent.total_amount = rent.get_total_cost
        rent.save()
    paystack_redirect_url = "{}?amount={}".format(
        reverse('paystack:verify_payment',
                args=[paystack_ref]), paystack_amount, rent)

    template = 'vehicle/confirm_booking.html'
    context = {'rent': rent,
                   'paystack_key': settings.PAYSTACK_PUBLIC_KEY,
                   'paystack_amount': paystack_amount,
                   'paystack_redirect_url': paystack_redirect_url
    }
    return render(request, template, context)


@csrf_exempt
def payment_done(request):
    rent_id = request.session.get('rent_id')
    rent = get_object_or_404(Rent, id=rent_id)
    return render(request, 'vehicle/invoice.html', {'rent': rent})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'canceled.html')


@login_required
def rented_vehicles(request):
    vehicles = Rent.objects.filter(customer=request.user)

    return render(
        request, 'rented_vehicles.html', {'vehicles': vehicles})


@login_required
def add_to_compare(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    if vehicle.compares.filter(id=request.user.id).exists():
        vehicle.compares.remove(request.user)
        messages.success(
            request, "You've removed the vehicle from comparison")
    else:
        vehicle.compares.add(request.user)
        messages.success(
            request, "You've added this vehicle for comparison")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def compare_vehicles(request):
    vehicles = Vehicle.objects.filter(
        is_available=True).filter(compares=request.user)[:3]
    return render(
        request, 'vehicle/compare.html', {'vehicles': vehicles})


@login_required
def vehicle_create(request):
    if not request.user.is_vendor:
        messages.info(
            request, "Login as a vendor to upload vehicle.")
        logout(request)
        return redirect('login')
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


@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk, vendor=request.user)
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


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk, vendor=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle successfully deleted')
        return redirect('vehicle_list')

    return render(request,
                  'vehicle/confirm_delete.html',
                  {'vehicle': vehicle})


# def check_availability(request, license_plate):
#     import datetime

#     date_of_booking = request.POST.get(
#         'date_of_booking', '')
#     date_of_return = request.POST.get(
#         'date_of_return', '')

#     date_of_booking = datetime.strptime(
#         date_of_booking, '%Y-%m-%d').date()
#     date_of_return = datetime.strptime(
#         date_of_return, '%Y-%m-%d').date()

#     rentvehicle = Rent.objects.filter(
#         license_plate=license_plate)
#     vehicle = Vehicle.objects.get(
#         license_plate=license_plate)

#     customer_email = request.session.get('user_email')
#     customer = Customer.objects.get(
#         customer_email=customer_email)

#     if date_of_booking < datetime.date.today():
#         Incorrect_dates = "Please give proper dates"
#         return render(
#             request, 'showdetails.html',
#             {'Incorrect_dates': Incorrect_dates,
#              'vehicle': vehicle, 'customer': customer})

#     if date_of_return < date_of_booking:
#         Incorrect_dates = "Please give proper dates"
#         return render(
#             request, 'showdetails_loggedin.html',
#             {'Incorrect_dates': Incorrect_dates,
#              'vehicle': vehicle, 'customer': customer})

#     days = (date_of_return - date_of_booking).days + 1
#     total = days * vehicle.price

#     rent_data = {
#         "date_of_booking": date_of_booking,
#         "date_of_return": date_of_return,
#         "days": days, "total": total
#     }

#     for rv in rentvehicle:
#         if (rv.date_of_booking >= date_of_booking and date_of_return >= rv.date_of_booking) or (date_of_booking >= rv.date_of_booking and date_of_return <= rv.date_of_return) or (date_of_booking <= rv.date_of_return and date_of_return >= rv.date_of_return):
#             if rv.isAvailable:
#                 Available = True
#                 Message = "Someone has requested for this vehicle from " + \
#                     str(rv.RentVehicle_Date_of_Booking) + \
#                     " to " + str(rv.RentVehicle_Date_of_Return)
#                 return render(
#                     request,
#                     'showdetails.html',
#                     {'Message': Message,
#                      'Available': Available,
#                      'vehicle': vehicle,
#                      'customer': customer,
#                      'rent_data': rent_data})

#             NotAvailable = True
#             return render(
#                 request,
#                 'showdetails.html',
#                 {'NotAvailable': NotAvailable,
#                  'dates': rv,
#                  'vehicle': vehicle,
#                  'customer': customer})

#         # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
#         #     Available = True
#         #     return render(request,'showdetails_loggedin.html',{'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})

#     Available = True

#     return render(
#         request, 'showdetails.html',
#         {'Available': Available, 'vehicle': vehicle,
#          'customer': customer, 'rent_data': rent_data})
