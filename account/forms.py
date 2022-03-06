from django import forms

from .models import User, VendorProfile, CustomerProfile
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class VendorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = False
        user.save()
        return user


class VendorProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['about'].widget.attrs.update(
            {'class': 'form-control', 'rows': '5'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['state'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = VendorProfile
        fields = ['company_name', 'address', 'phone_number',
                  'city', 'state', 'image', 'about']


class CustomerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['license'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['government_id'].widget.attrs.update(
            {'class': 'form-control', 'rows': '5'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['state'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = CustomerProfile
        fields = ['government_id', 'address', 'phone_number',
                  'city', 'state', 'image', 'license']


class VerifyForm(forms.Form):
    code = forms.CharField(
        label='Enter verification code',
        max_length=8, required=True)
