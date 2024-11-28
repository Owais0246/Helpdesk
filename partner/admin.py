"""
Django admin configuration for managing the Partner, Engineer, Location, 
and EngineerLocation models.

This module registers the following models in the Django admin:
- Partner: Represents a business partner.
- Engineer: Represents an engineer associated with a partner.
- Location: Represents a geographical location.
- EngineerLocation: Represents the relationship between engineers and locations.
"""

from django.contrib import admin
from .models import Partner, Engineer, State, City, Region, EngineerLocation

# Registering models with the Django admin site
admin.site.register(Partner)
admin.site.register(Engineer)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(EngineerLocation)
