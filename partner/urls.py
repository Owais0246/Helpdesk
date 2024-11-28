from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.partner_create, name='partner_create'),
    path('partner/<int:partner_id>/', views.partner_detail, name='partner_detail'),
    path('', views.partner_list, name='partner_list'),  # Optional view for listing partners
    # URL for rendering the location creation form
    path('create-location/', views.location_create_view, name='create_location'),

    path('get-states/', views.get_states, name='get_states'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('get-regions/', views.get_regions, name='get_regions'),
    path('locations/', views.location_list, name='location_list'),

    path('edit-location/<int:region_id>/', views.edit_location, name='edit_location'),

]
