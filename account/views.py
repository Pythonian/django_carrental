from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from . import verify
from vehicle.models import Vehicle
from carrental.utils import mk_paginator
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import (
    VendorSignUpForm, CustomerSignUpForm, VendorProfileForm,
    CustomerProfileForm, VerifyForm)


class VendorSignUpView(CreateView):
    model = User
    form_class = VendorSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'a vendor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('vendor_create_profile')


@login_required
def vendor_profile(request):
    return render(request, 'vendor/profile.html', {})


@login_required
def vendor_create_profile(request):
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            messages.success(
                request, 'Your profile was successully created. Please upload your first car details for rental')
            return redirect('vehicle:create')
        else:
            messages.warning(
                request, 'Error creating your profile. Please check below.')
    else:
        form = VendorProfileForm()

    return render(request,
                  'vendor/form.html',
                  {'form': form, 'create': True})


@login_required
def vendor_update_profile(request):
    if request.method == 'POST':
        form = VendorProfileForm(
            request.POST, request.FILES, instance=request.user.vendor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successully updated.')
            return redirect('vendor_update_profile')
        else:
            messages.error(
                request, 'Error updating your profile. Please check below.')
    else:
        form = VendorProfileForm(
            instance=request.user.vendor_profile)

    return render(request,
                  'vendor/form.html',
                  {'form': form})


@login_required
def vendor_manage_vehicles(request):
    vehicles = Vehicle.objects.filter(vendor=request.user)
    vehicles = mk_paginator(request, vehicles, 2)
    return render(
        request, 'vendor/vehicles.html', {'vehicles': vehicles})


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'a customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer_create_profile')


@login_required
def customer_create_profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            verify.send(form.cleaned_data.get('phone_number'))
            messages.success(
                request, 'Profile created. Please verify your phone number')
            return redirect('customer_verification')
        else:
            messages.warning(
                request, 'Error creating your profile. Please check below.')
    else:
        form = CustomerProfileForm()

    return render(request,
                  'customer/form.html',
                  {'form': form, 'create': True})


@login_required
def customer_verification(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.customer_profile.phone_number, code):
                request.user.customer_profile.verified = True
                request.user.customer_profile.save()
                return redirect('home')
    else:
        form = VerifyForm()
    return render(request, 'customer/verify.html', {'form': form})


@login_required
def customer_update_profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(
            request.POST, request.FILES,
            instance=request.user.customer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successully updated.')
            return redirect('customer_update_profile')
        else:
            messages.error(
                request, 'Error updating your profile. Please check below.')
    else:
        form = CustomerProfileForm(
            instance=request.user.customer_profile)

    return render(request,
                  'customer/form.html',
                  {'form': form})
