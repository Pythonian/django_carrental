import datetime
from django import forms

from .models import Vehicle, Rent


class VehicleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        # self.fields['name'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['model'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['color'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['no_of_seats'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'form-control', 'rows': '5'})
        # self.fields['car_type'].widget.attrs.update(
        #     {'class': 'form-select'})
        # self.fields['gear_type'].widget.attrs.update(
        #     {'class': 'form-select'})
        # self.fields['fuel_type'].widget.attrs.update(
        #     {'class': 'form-select'})
        # self.fields['price'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['image'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['license_plate'].widget.attrs.update(
        #     {'class': 'form-control'})
        # self.fields['area'].widget.attrs.update(
        #     {'class': 'form-select'})

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
    date_of_booking = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control'}))
    date_of_return = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Rent
        fields = ['date_of_booking', 'date_of_return']

    def clean_date_of_return(self):
        date_of_booking = self.cleaned_data['date_of_booking']
        date_of_return = self.cleaned_data['date_of_return']
        today_date = datetime.date.today()

        if (date_of_booking or date_of_return) < today_date:
            # both dates must not be in the past
            raise forms.ValidationError(
                "Selected dates are incorrect, please select again")
        elif date_of_booking >= date_of_return:
            # TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
            raise forms.ValidationError("Selected dates are wrong")
        return date_of_return
