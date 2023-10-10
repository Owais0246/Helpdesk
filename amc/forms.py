from django import forms
from .models import Amc
from masters.models import Product, Location
from django.forms import formset_factory



class CreateAmcForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ('start_date',
                  'expiry','description','sla','escalation_matrix_1','escalation_matrix_2','escalation_matrix_3','escalation_matrix_4')
        
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
        
        

class ProductForm(forms.Form):
    product_name = forms.CharField(max_length=200)
    part_number = forms.CharField(max_length=200)
    serial_number = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 15}), required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    
    
ProductFormSet = formset_factory(ProductForm, extra=1)

class AmcForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ['company', 'description', 'start_date', 'expiry', 'sla', 'escalation_matrix_1', 'escalation_matrix_2', 'escalation_matrix_3', 'escalation_matrix_4']

    products = ProductFormSet()