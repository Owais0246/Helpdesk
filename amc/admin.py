from django.contrib import admin
from .models import Amc, Service, Source
# Register your models here.
admin.site.register([Amc, Service, Source])