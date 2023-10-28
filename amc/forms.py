from django import forms
from .models import Amc
from masters.models import Product, Location
from django.forms import inlineformset_factory



class CreateAmcForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ('start_date','expiry','amc_description','sla',
                  'escalation_matrix_1','escalation_matrix_2',
                  'escalation_matrix_3','escalation_matrix_4',)
        
        labels = {
            'loc_name': 'Location Name',
            'loc_company': 'Company',
            'loc_poc_contact_no': 'POC\'s Phone Number',
            'loc_address': 'Address',

        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','part_number','serial_number','description','location']
        
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'part_number', 'serial_number', 'description', 'location']
    
    
ProductFormSet = inlineformset_factory(Amc, Product, form=ProductForm, extra=1)

class AMCForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ['amc_description', 'start_date', 'expiry', 'sla', 'escalation_matrix_1', 'escalation_matrix_2', 'escalation_matrix_3', 'escalation_matrix_4']