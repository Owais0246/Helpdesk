from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_contact_no', 'user_company', 'user_loc', 'is_service_admin', 'is_salesperson', 'is_service_agent', 'is_customer_user', 'is_customer_admin', 'is_field_engineer', 'is_sr_engineer')
    list_filter = ('user_company', 'user_loc', 'is_service_admin', 'is_salesperson', 'is_service_agent', 'is_customer_user', 'is_customer_admin', 'is_field_engineer', 'is_sr_engineer')
    search_fields = ('username', 'email', 'user_contact_no')
    readonly_fields = ('aadhaar_no', 'covid_cert')

admin.site.register(User, UserAdmin)
