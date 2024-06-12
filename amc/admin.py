"""
Admin configuration for AMC (Annual Maintenance Contract) related models.

This file defines the admin configurations for the AMC, Source, and Service models. 
It customizes the appearance and behavior of the admin interface for these models, 
providing features such as list display, filtering, searching, and hierarchical navigation.

Classes:
    AmcAdmin: Customizes the appearance and behavior of the AMC admin interface.
"""

from django.contrib import admin
from .models import Amc, Source, Service

class AmcAdmin(admin.ModelAdmin):
    """
    Customizes the appearance and behavior of the AMC (Annual Maintenance Contract) admin interface.
    """
    list_display = ('uuid', 'company', 'amc_description', 'start_date', 'expiry', 'salesperson')
    list_filter = ('company', 'start_date', 'expiry', 'salesperson')
    search_fields = ('uuid', 'amc_description', 'salesperson__username')
    date_hierarchy = 'start_date'

admin.site.register(Amc, AmcAdmin)
admin.site.register(Source)
admin.site.register(Service)
