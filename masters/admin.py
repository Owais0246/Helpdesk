from django.contrib import admin
from .models import Company, Location, Product

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name_with_suffix', 'company_contact_no', 'address', 'is_customer', 'is_self_company')
    
    def company_name_with_suffix(self, obj):
        return f'{obj.company_name} ({obj.company_suffix})'
    company_name_with_suffix.short_description = 'Company Name'

class LocationAdmin(admin.ModelAdmin):
    list_display = ('loc_name', 'loc_company', 'loc_poc_email', 'loc_poc_contact_no', 'loc_address')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'model_number', 'serial_number', 'created_on', 'description', 'location', 'amc', 'amount')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Product, ProductAdmin)
