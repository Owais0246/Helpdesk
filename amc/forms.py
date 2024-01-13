from django import forms
from .models import Amc
from masters.models import Product, Location
from django.forms import inlineformset_factory



from django import forms
from .models import Amc

class CreateAmcForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ('start_date', 'expiry', 'amc_description', 'sla',
                  'escalation_matrix_1', 'escalation_matrix_2',
                  'escalation_matrix_3', 'escalation_matrix_4',
                  'sla_file', 'invoice', 'po', 'log', 'config', 'file')

        labels = {
            'amc_description': 'AMC Description',
            'start_date': 'Start Date',
            'expiry': 'Expiry Date',
            'sla': 'SLA',
            'escalation_matrix_1': 'Escalation Matrix 1',
            'escalation_matrix_2': 'Escalation Matrix 2',
            'escalation_matrix_3': 'Escalation Matrix 3',
            'escalation_matrix_4': 'Escalation Matrix 4',
            'sla_file': 'SLA File',
            'invoice': 'Invoice File',
            'po': 'Purchase Order File',
            'log': 'Log File',
            'config': 'Config File',
            'file': 'Other File',
        }

    def __init__(self, *args, **kwargs):
        super(CreateAmcForm, self).__init__(*args, **kwargs)
        # Add any additional customization here if needed
        # For example, you can set required or add custom validation for specific fields
        self.fields['sla_file'].required = False
        self.fields['invoice'].required = False
        self.fields['po'].required = False
        self.fields['log'].required = False
        self.fields['config'].required = False
        self.fields['file'].required = False

        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','model_number','serial_number','description','amount','location']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model Number'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
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
        fields = ('start_date', 'expiry', 'amc_description', 'sla',
                  'escalation_matrix_1', 'escalation_matrix_2',
                  'escalation_matrix_3', 'escalation_matrix_4',
                  'sla_file', 'invoice', 'po', 'log', 'config', 'file','salesperson', 'source', 'service_provider')

        labels = {
            'amc_description': 'AMC Description',
            'start_date': 'Start Date',
            'expiry': 'Expiry Date',
            'sla': 'SLA',
            'escalation_matrix_1': 'Escalation Matrix 1',
            'escalation_matrix_2': 'Escalation Matrix 2',
            'escalation_matrix_3': 'Escalation Matrix 3',
            'escalation_matrix_4': 'Escalation Matrix 4',
            'sla_file': 'SLA File',
            'invoice': 'Invoice File',
            'po': 'Purchase Order File',
            'log': 'Log File',
            'config': 'Config File',
            'file': 'Other File',
            'salesperson':'Sales Person'
        }
