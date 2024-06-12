"""
URL patterns for the reports app.

Attributes:
    urlpatterns (list): List of URL patterns.

"""
from django.urls import path
from . import views

# from .views import get_company_details, get_product_details, get_user_details

urlpatterns = [
    path('amc-report/', views.amc_list, name='amc_report'),
    path('amc-report/<int:amc_id>/', views.amc_detail, name='amc_detail'),
    
    ]
