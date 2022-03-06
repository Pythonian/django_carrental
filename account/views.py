from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from vehicle.models import Vehicle

from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import (
    VendorSignUpForm, CustomerSignUpForm, VendorProfileForm)


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
        return redirect('home')


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
    return render(
        request, 'vendor/vehicles.html', {'vehicles': vehicles})
