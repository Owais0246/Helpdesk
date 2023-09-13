from django import forms
from .models import Company,Location,Product


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name','company_contact_no','address']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['loc_name','loc_poc_email','loc_poc_contact_no','loc_address']
        labels = {
            'loc_name': 'Location Name',
            'loc_poc_email': 'POC\'s Email Id',
            'loc_poc_contact_no': 'POC\'s Phone Number',
            'loc_address': 'Address',
            
        }
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','part_number','serial_number','description')
        # ,'location'

        
     
    