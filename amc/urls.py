"""
URL patterns for the AMC (Annual Maintenance Contract) application.

This module defines URL patterns for various views related to AMC operations,
such as creating, listing, updating, and detailing AMC instances.

Each URL pattern is associated with a specific view function or class-based view.
"""
from django.urls import path
from . import views
from .views import (AmcListView,AmcUpdateView)


urlpatterns = [
    #Amc urls
    path('amc_add/<int:pk>', views.create_amc, name="AmcCreate"),
    path('amc_list', AmcListView.as_view(), name="AmcList"),
    path('amc_update/<int:pk>', AmcUpdateView.as_view(), name="AmcUpdate"),
    path('amc_detail/<int:pk>', views.amc_detail, name="AmcDetail"),
    path('load_contact_person', views.load_contact_person, name="LoadContactPerson"),

    ]
