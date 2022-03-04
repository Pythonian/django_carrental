from django.contrib.auth import login
from .models import User

from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import VendorSignUpForm, CustomerSignUpForm


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
