"""
Configuration for AMC (Annual Maintenance Contract) app.

This module contains the configuration settings for the AMC app, 
including the default auto-generated primary key field
and the name of the app.

Classes:
    AmcConfig: Configuration class for the AMC app.
"""

from django.apps import AppConfig


class AmcConfig(AppConfig):
    """
    Configuration class for the AMC (Annual Maintenance Contract) app.

    This class defines configuration settings for the AMC app, 
    such as the default auto-generated primary key field,
    and the name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'amc'
