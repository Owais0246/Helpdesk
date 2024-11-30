from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.partner_create, name='partner_create'),
    path('partner/<int:partner_id>/', views.partner_detail, name='partner_detail'),
    path('', views.partner_list, name='partner_list'),
    path('create-location/', views.location_create_view, name='create_location'),
    
    path('get-states/', views.get_states, name='get_states'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('get-regions/', views.get_regions, name='get_regions'),
    path('locations/', views.location_list, name='location_list'),
    path('create-engineer/<int:partner_id>/', views.create_engineer, name='create_engineer'),
    path('edit-location/<int:region_id>/', views.edit_location, name='edit_location'),
        # URL for state detail page
    path('state/<int:state_id>/', views.state_detail, name='state_detail'),

    # URL for city detail page
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),

    # URL for region detail page
    path('region/<int:region_id>/', views.region_detail, name='region_detail'),
]
