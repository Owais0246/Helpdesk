from django.db import models

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=50, help_text='Enter your Company Name')
    company_contact_no = models.IntegerField(blank=True, help_text='Enter Company Phone Number')
    address = models.TextField()

    def __str__(self):
        return self.company_name


class Location(models.Model):
    loc_name = models.CharField(max_length=50, help_text='Enter Branch Name')
    loc_company = models.ForeignKey(Company, on_delete=models.PROTECT, help_text='Select Company Name')
    loc_poc_contact_no =models.IntegerField(blank=True, help_text='Enter Company Phone Number')
    loc_address = models.TextField()

    def __str__(self):
        return self.loc_name


class Product(models.Model):
    product_name=models.CharField(max_length=200,blank=False)    
    part_number=models.CharField(max_length=200,blank=False)    
    serial_number=models.CharField(max_length=200,blank=False)    
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200,blank=True)
    location= models.CharField(max_length=50)
    
    def __str__(self):
        return self.product_name


