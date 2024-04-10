from django.urls import path
from masters import views
from .views import (CustomerCreateView,CustomerListView,CustomerUpdateView,
                    LocationCreateView,LocationListView,LocationUpdateView,
                    ProductCreateView,ProductListView,ProductUpdateView, 
                    get_company_details, get_product_details, get_user_details )
# from .views import get_company_details, get_product_details, get_user_details  # Import the view you created


urlpatterns = [
    #Company urls
    path('company/add', views.create_customer, name="CompanyCreate"),
    path('company/list', views.customer_list, name="CompanyList"),
    path('company/update/<int:pk>', CustomerUpdateView.as_view(), name="CompanyUpdate"),
    path('company/detail/<int:company_pk>', views.customer_detail, name="CompanyDetail"),
    path('get_company_details/', get_company_details, name='get_company_details'),
    path('get_product_details/', get_product_details, name='get_product_details'),
    path('get_user_details/', get_user_details, name='get_user_details'),

    
    
    
    path('create-user/<int:company_pk>/<int:location_pk>', views.create_customer_user, name="CreateCustomerUser"),
    
    #Location Urls
    path('location/add', LocationCreateView.as_view(), name="CreateLocation"),
    path('location/list', LocationListView.as_view(), name="LocationList"),
    path('location/update/<int:pk>', LocationUpdateView.as_view(), name="LocationUpdate"),
    path('location/detail/<int:pk>', views.LocationDetail, name="LocationDetail"),
    path('location/load-location', views.LoadLocation, name="LoadLocation"),
    
    
    #Product
    path('product/add', ProductCreateView.as_view(), name="CreateProduct"),
    path('product/list', ProductListView.as_view(), name="ProductList"),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name="ProductUpdate"),
    path('product/detail/<int:pk>', views.ProductDetail, name="ProductDetail"),
    
    ]
