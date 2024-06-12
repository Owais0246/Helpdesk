"""
Admin configuration for the support app.

This module contains admin configurations for the Company, 
Location, and Product models in the support app.

Classes:
    CompanyAdmin: Admin configuration for the Company model.
    LocationAdmin: Admin configuration for the Location model.
    ProductAdmin: Admin configuration for the Product model.

"""

from django.contrib import admin
from .models import Company, Location, Product

class CompanyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Company model.

    This class defines the list display fields and custom methods for the Company admin interface.

    Attributes:
        list_display (tuple): A tuple of fields to display in the Company list view.

    Methods:
        company_name_with_suffix: Custom method to display the company name with its suffix.

    """
    list_display = ('company_name_with_suffix', 'company_contact_no',
                    'address', 'is_customer', 'is_self_company') 

    def company_name_with_suffix(self, obj):
        """
        Custom method to display the company name with its suffix.

        Args:
            self: The CompanyAdmin instance.
            obj: The Company object.

        Returns:
            str: The formatted company name with suffix.
        """
        return f'{obj.company_name} ({obj.company_suffix})'
    company_name_with_suffix.short_description = 'Company Name'


class LocationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Location model.

    This class defines the list display fields for the Location admin interface.

    Attributes:
        list_display (tuple): A tuple of fields to display in the Location list view.

    """
    list_display = ('loc_name', 'loc_company', 'loc_poc_email', 'loc_poc_contact_no', 'loc_address')

class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.

    This class defines the list display fields for the Product admin interface.

    Attributes:
        list_display (tuple): A tuple of fields to display in the Product list view.

    """
    list_display = ('product_name', 'model_number', 'serial_number',
                    'created_on', 'description', 'location', 'amc', 'amount')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Product, ProductAdmin)
