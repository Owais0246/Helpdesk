"""
Module: users.models

This module defines the database models related to user management in the application.

Classes:
    User: Represents a user of the system, extending Django's AbstractUser model.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from masters.models import Company,Location

# Create your models here.

# USER
class User(AbstractUser):
    """
    A custom user model representing users of the system.
    """
    email = models.EmailField()
    user_contact_no = models.BigIntegerField(null=True,blank=True)
    user_company= models.ForeignKey(Company,on_delete=models.CASCADE, null=True)
    user_loc = models.ForeignKey(Location,on_delete=models.CASCADE, null=True)
    is_service_admin=models.BooleanField(default=False)
    is_salesperson=models.BooleanField(default=False)
    is_service_agent=models.BooleanField(default=False)
    is_customer_user=models.BooleanField(default=False)
    is_customer_admin=models.BooleanField(default=False)
    is_field_engineer=models.BooleanField(default=False)
    is_sr_engineer=models.BooleanField(default=False)
    aadhaar_no = models.FileField(upload_to='user/', null=True, blank=True)
    covid_cert = models.FileField(upload_to='user/', null=True, blank=True)

    def __str__(self):
        """
        Returns the username of the user as a string.
        """
        return f'{self.first_name} {self.last_name}'
    