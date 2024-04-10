from django.contrib import admin
from .models import Amc, Source, Service

class AmcAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'company', 'amc_description', 'start_date', 'expiry', 'salesperson')
    list_filter = ('company', 'start_date', 'expiry', 'salesperson')
    search_fields = ('uuid', 'amc_description', 'salesperson__username')
    date_hierarchy = 'start_date'

admin.site.register(Amc, AmcAdmin)
admin.site.register(Source)
admin.site.register(Service)
