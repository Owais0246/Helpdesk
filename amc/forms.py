"""
Forms for AMC (Annual Maintenance Contract) related functionality.

This module contains various forms used in the AMC app, including forms for creating AMC instances,
products associated with AMC, and the AMC itself.

Classes:
    CreateAmcForm: Form for creating an AMC instance.
    ProductForm: Form for creating a product associated with an AMC.
    AMCForm: Form for creating or updating an AMC instance.
"""

from django import forms
from django.forms import inlineformset_factory
from masters.models import Product
from .models import Amc


class CreateAmcForm(forms.ModelForm):
    """
        Form for creating an AMC instance.

        This form allows users to create an AMC instance by providing details such as start date,
        expiry date, description, service level agreement (SLA), escalation matrices.
    """

    class Meta:
        """
        Meta class for CreateAmcForm.
        Defines metadata options for the CreateAmcForm class.
        """
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
        """
        Initialize the CreateAmcForm instance.
        Sets some form fields as not required and adds customizations to the form fields.
        """
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
    """
    Form for creating a product associated with an AMC.

    This form allows users to create a product associated with an AMC by providing details such as
    product name, model number, serial number, description, amount, and location.
    """
    class Meta:
        """
        Meta class for ProductForm.
        Defines metadata options for the ProductForm class.
        """
        model = Product
        fields = ['product_name','model_number','serial_number','description','amount','location']
        widgets = {
            'product_name': 
                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'model_number': 
                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model Number'}),
            'serial_number': 
                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'description': 
                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'amount': 
                forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'location': 
                forms.Select(attrs={'class': 'form-select'}),
        }

ProductFormSet = inlineformset_factory(Amc, Product, form=ProductForm, extra=1, can_delete=True)

class AMCForm(forms.ModelForm):
    """
    Form for creating or updating an AMC instance.

    This form allows users to create or update an AMC instance by providing details such as 
    start date, expiry date, description, service level agreement (SLA), escalation matrices, 
    various files, salesperson, source, and service provider.
    """

    class Meta:
        """
        Meta class for AMCForm.

        Defines metadata options for the AMCForm class.
        """
        model = Amc
        fields = ('start_date', 'expiry', 'amc_description', 'sla',
                  'escalation_matrix_1', 'escalation_matrix_2',
                  'escalation_matrix_3', 'escalation_matrix_4',
                  'sla_file', 'invoice', 'po', 'log', 'config', 
                  'file','salesperson', 'source', 'service_provider')

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
