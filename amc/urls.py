from django.urls import path
from . import views
from .views import (AmcListView,AmcUpdateView)


urlpatterns = [
    #Amc urls
    path('amc_add/<int:pk>', views.create_amc, name="AmcCreate"),
    
    path('amc_list', AmcListView.as_view(), name="AmcList"),
    path('amc_update/<int:pk>', AmcUpdateView.as_view(), name="AmcUpdate"),
    path('amc_detail/<int:pk>', views.AmcDetail, name="AmcDetail"),
    path('load_contact_person', views.load_contact_person, name="LoadContactPerson"),
    
    ]

