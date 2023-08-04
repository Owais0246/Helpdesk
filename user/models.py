from django.db import models
from django.contrib.auth.models import AbstractUser
from masters.models import Company,Location

# Create your models here.

# USER
class User(AbstractUser):
    
    email = models.EmailField()
    contact_no = models.IntegerField(null=True)
    user_type = models.CharField(max_length=30,choices=(("Internal","Internal"),("Customer","Customer")))
    user_company= models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    user_loc = models.ForeignKey(Location,on_delete=models.CASCADE, null=True)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)

    
    
