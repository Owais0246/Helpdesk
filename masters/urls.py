from django.urls import path
from masters import views
from .views import (CompanyCreateView,CompanyListView,CompanyUpdateView,
                    LocationCreateView,LocationListView,LocationUpdateView,
                    ProductCreateView,ProductListView,ProductUpdateView)


urlpatterns = [
    #Company urls
    path('company/add', CompanyCreateView.as_view(), name="CompanyCreate"),
    path('company/list', CompanyListView.as_view(), name="CompanyList"),
    path('company/update/<int:pk>', CompanyUpdateView.as_view(), name="CompanyUpdate"),
    path('company/detail/<int:pk>', views.CompanyDetail, name="CompanyDetail"),
    
    #Location Urls
    path('location/add', LocationCreateView.as_view(), name="CreateLocation"),
    path('location/list', LocationListView.as_view(), name="LocationList"),
    path('location/update/<int:pk>', LocationUpdateView.as_view(), name="LocationUpdate"),
    path('location/detail/<int:pk>', views.LocationDetail, name="LocationDetail"),
    
    #Product
    path('product/add', ProductCreateView.as_view(), name="CreateProduct"),
    path('product/list', ProductListView.as_view(), name="ProductList"),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name="ProductUpdate"),
    path('product/detail/<int:pk>', views.ProductDetail, name="ProductDetail"),
    
    ]
