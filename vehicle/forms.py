from django import forms

from .models import Vehicle, Rent


class VehicleForm(forms.ModelForm):
    error_css_class = 'text-danger'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['model'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['color'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['no_of_seats'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'rows': '5'})
        self.fields['car_type'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['gear_type'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['fuel_type'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['license_plate'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['area'].widget.attrs.update(
            {'class': 'form-select'})

    class Meta:
        model = Vehicle
        exclude = ['vendor', 'created', 'updated', 'is_available']

    # def clean_license_plate(self):
    #     try:
    #         Vehicle.objects.get(
    #             license_plate=self.cleaned_data['license_plate'])
    #     except Vehicle.DoesNotExist:
    #         return self.cleaned_data['license_plate']
    #     raise forms.ValidationError("This vehicle has been uploaded already.")


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        exclude = ['vehicle', 'customer', 'vendor', 'created', 'updated']
