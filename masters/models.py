from django.db import models




# Create your models here.

class Company(models.Model):
    
    company_name = models.CharField(max_length=50, help_text='Enter your Company Name')
    company_contact_no =models.BigIntegerField(blank=True, help_text='Enter Company Phone Number')
    address = models.TextField()
    company_suffix= models.CharField(max_length=10, help_text='Enter your Company Suffix',null=True,blank=True)
    is_customer = models.BooleanField(default=False)
    is_self_company = models.BooleanField(default=False)
    # salesperson = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)    
    

    def __str__(self):
        return f'{self.company_name}'


class Location(models.Model):
    loc_company = models.ForeignKey(Company, on_delete=models.PROTECT, help_text='Select Company Name')
    loc_name = models.CharField(max_length=50, help_text='Enter Branch Name')
    loc_poc_email= models.EmailField(max_length=254)
    loc_poc_contact_no =models.BigIntegerField(blank=True, help_text='Enter Company Phone Number')
    loc_address = models.TextField()

    def __str__(self):
        return f'{self.loc_name}'

class Product(models.Model):
    product_name=models.CharField(max_length=200,blank=False)    
    model_number=models.CharField(max_length=200,blank=False)    
    serial_number=models.CharField(max_length=200,blank=False)    
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255,null=True, blank=True)
    location= models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True, related_name='asset_location')
    amc = models.ForeignKey('amc.Amc', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    amount = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return self.product_name +" - " + self.serial_number


