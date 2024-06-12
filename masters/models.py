"""
Module containing models for the support app.

This module defines the database models used in the support app of the Django project.

Classes:
    Company: Model representing a company.
    Location: Model representing a location associated with a company.
    Product: Model representing a product.
"""
from django.db import models


class Company(models.Model):
    """
    Model representing a company.

    Attributes:
        company_name (CharField): The name of the company.
        company_contact_no (BigIntegerField): The phone number of the company.
        address (TextField): The address of the company.
        company_suffix (CharField): The suffix of the company's name.
        is_customer (BooleanField): Indicates if the company is a customer.
        is_self_company (BooleanField): Indicates if the company is self-owned.
    """
    company_name = models.CharField(max_length=50, help_text='Enter your Company Name')
    company_contact_no =models.BigIntegerField(blank=True, help_text='Enter Company Phone Number')
    address = models.TextField()
    company_suffix= models.CharField(max_length=10, help_text='Enter your Company Suffix',
                                     null=True,blank=True)
    is_customer = models.BooleanField(default=False)
    is_self_company = models.BooleanField(default=False)
    # salesperson = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        """
        String representation of the company.
        """
        return f'{self.company_name}'

class Location(models.Model):
    """
    Model representing a location.

    Attributes:
        loc_company (ForeignKey): The company associated with the location.
        loc_name (CharField): The name of the branch.
        loc_poc_email (EmailField): The email address of the point of contact.
        loc_poc_contact_no (BigIntegerField): The phone number of the point of contact.
        loc_address (TextField): The address of the location.
    """
    loc_company = models.ForeignKey(Company, on_delete=models.PROTECT,
                                    help_text='Select Company Name')
    loc_name = models.CharField(max_length=50, help_text='Enter Branch Name')
    loc_poc_email= models.EmailField(max_length=254)
    loc_poc_contact_no =models.BigIntegerField(blank=True, help_text='Enter Company Phone Number')
    loc_address = models.TextField()

    def __str__(self):
        """
        String representation of the location.
        """
        return f'{self.loc_company} - {self.loc_name}'
    
class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        product_name (CharField): The name of the product.
        model_number (CharField): The model number of the product.
        serial_number (CharField): The serial number of the product.
        created_on (DateTimeField): The date and time when the product was created.
        description (CharField): The description of the product.
        location (ForeignKey): The location associated with the product.
        amc (ForeignKey): The AMC (Annual Maintenance Contract) associated with the product.
        amount (IntegerField): The amount of the product.
    """
    product_name=models.CharField(max_length=200,blank=False)
    model_number=models.CharField(max_length=200,blank=False)
    serial_number=models.CharField(max_length=200,blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255,null=True, blank=True)
    location= models.ForeignKey(Location, on_delete=models.PROTECT,
                                null=True, blank=True, related_name='asset_location')
    amc = models.ForeignKey('amc.Amc', on_delete=models.CASCADE, related_name='products',
                            null=True, blank=True)
    amount = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        """
        String representation of the profuct.
        """
        return f'{self.product_name} - {self.serial_number}'
