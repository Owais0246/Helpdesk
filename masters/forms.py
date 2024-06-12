"""
Module containing forms for the support app.

This module defines forms used for creating or 
updating company, location, and product records
in the support app of the Django project.

Classes:
    CompanyForm: Form for creating or updating a company.
    LocationForm: Form for creating or updating a location.
    ProductForm: Form for creating or updating a product.
"""

from django import forms
from .models import Company,Location,Product

class CompanyForm(forms.ModelForm):
    """
    Form for creating or updating a company.

    This form is used to create or update company records in the database.
    """
    class Meta:
        """
        Meta: Inner class containing metadata for the CompanyForm.
        """
        model = Company
        fields = ['company_name','company_contact_no','address','company_suffix']


class LocationForm(forms.ModelForm):
    """
    Form for creating or updating a location.

    This form is used to create or update location records in the database.
    """
    class Meta:
        """
        Meta: Inner class containing metadata for the LocationForm.
        """
        model = Location
        fields = ['loc_name','loc_poc_email','loc_poc_contact_no','loc_address']
        labels = {
            'loc_name': 'Location Name',
            'loc_poc_email': 'POC\'s Email Id',
            'loc_poc_contact_no': 'POC\'s Phone Number',
            'loc_address': 'Address',
        }


class ProductForm(forms.ModelForm):
    """
    Form for creating or updating a product.

    This form is used to create or update product records in the database.
    """
    class Meta:
        """
        Meta: Inner class containing metadata for the ProductForm.
        """
        model = Product
        fields = ('product_name','model_number','serial_number','description')
        # ,'location'
