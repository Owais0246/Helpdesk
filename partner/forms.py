from django import forms
from .models import Partner, Engineer, State, City, Region

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'contact_name', 'email_address', 'contact_no']
        widgets = {
            'contact_no': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Enter email address'})
        }


class EngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields = ['name', 'email', 'contact_no', 'expertise', 'region']
        widgets = {
            'region': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }


class LocationForm(forms.Form):
    state = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    region = forms.CharField(max_length=255)
    pin = forms.CharField(max_length=6)