"""
Django models for managing partners, engineers, locations, and their relationships.

This module defines the following models:
- Partner: Represents a business partner with contact details.
- Engineer: Represents an engineer associated with a partner, with expertise and contact details.
- Location: Represents a geographical location with state, city, and region.
- EngineerLocation: Represents the relationship between engineers and locations they serve.
"""
from django.db import models


class Partner(models.Model):
    """
    A model representing a business partner.
    """
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    contact_no = models.CharField(max_length=20)

    def __str__(self):
        """
        Return the name of the partner as a string.
        """
        return str(self.name)


class Engineer(models.Model):
    """
    A model representing an engineer associated with a partner.
    """
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="engineers")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_no = models.CharField(max_length=20)
    expertise = models.TextField()

    def __str__(self):
        """
        Return the name of the engineer as a string.
        """
        return str(self.name)


class State(models.Model):
    """
    A model representing a state.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Return the name of the state as a string.
        """
        return str(self.name)


class City(models.Model):
    """
    A model representing a city, which is associated with a state.
    """
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Return the name of the city as a string.
        """
        return str(self.name)


class Region(models.Model):
    """
    A model representing a region, which is associated with a city.
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Return the name of the region as a string.
        """
        return str(self.name)


class EngineerLocation(models.Model):
    """
    A model representing the relationship between an engineer and a location.
    """
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        """
        Meta class to ensure unique combination of engineer and location.
        """
        unique_together = ('engineer', 'region')

    def __str__(self):
        """
        Return a string representation of the engineer's service location.
        """
        return str(f"{self.engineer.name} serves {self.region}")
