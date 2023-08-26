from django.db import models
from masters.models import Company,Location,Product
from user.models import User


# Create your models here.

class Amc(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT, null=True,blank=True)
    location = models.ForeignKey(Location,on_delete=models.PROTECT, null=True,blank=True)
    # user = models.ForeignKey(User,on_delete=models.PROTECT, null=True,blank=True)    
    product= models.ForeignKey(Product,on_delete=models.PROTECT, null=True,blank=True)
    description = models.CharField(max_length=200,blank=True)
    startdate = models.DateTimeField()
    duration= models.IntegerField()
    
    def __str__(self):
        return str(self.company) +str(self.pk)