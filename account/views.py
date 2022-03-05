from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

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
        return redirect('home')


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
def vendor_update_profile(request):
    if request.method == 'POST':
        profile_form = VendorProfileForm(
            request.POST, instance=request.user.vendor_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successully updated.')
            return redirect('vendor_profile')
        else:
            messages.error(
                request, 'Error updating your profile. Please check below.')
    else:
        profile_form = VendorProfileForm(
            instance=request.user.vendor_profile)

    return render(request,
                  'vendor_profile_form.html',
                  {'profile_form': profile_form})
