"""
URL configuration for the dashboard app.

This module defines URL patterns for the dashboard app. 
It maps URLs to view functions defined in the views module.

Attributes:
    urlpatterns (list): A list of URL patterns defined for the dashboard app.

Example:
    To include these URL patterns in the project's main URL configuration (usually in urls.py), 
    you can use the `include` function:

    .. code-block:: python

        from django.urls import include, path

        urlpatterns = [
            path('dashboard/', include('dashboard.urls')),
        ]
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard')
]
