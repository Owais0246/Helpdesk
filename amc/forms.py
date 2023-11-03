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
        fields = ['product_name','model_number','serial_number','description','location']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model Number'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }
    # def __init__(self, company, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #     # Filter locations based on the selected company
    #     self.fields['location'].queryset = Location.objects.filter(loc_company=company)
        

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'model_number', 'serial_number', 'description', 'location']
        
        
    
    

ProductFormSet = inlineformset_factory(Amc, Product, form=ProductForm, extra=1, can_delete=True)

class AMCForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ['amc_description', 'start_date', 'expiry', 'sla', 'escalation_matrix_1', 'escalation_matrix_2', 
                  'escalation_matrix_3', 'escalation_matrix_4' , 'file'] 