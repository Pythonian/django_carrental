from django import forms 

from .models import Vehicle, Rent


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['vendor', 'created', 'updated']

    def clean_license_plate(self):
        try:
            Vehicle.objects.get(
                license_plate=self.cleaned_data['license_plate'])
        except Vehicle.DoesNotExist:
            return self.cleaned_data['license_plate']
        raise forms.ValidationError("This vehicle has been uploaded already.")


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        exclude = ['vehicle', 'customer', 'vendor', 'created', 'updated']
