from django.db import models
from masters.models import Company,Location,Product
from user.models import User


# Create your models here.

class Amc(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT)
    location = models.ForeignKey(Location,on_delete=models.PROTECT)
    # user = models.ForeignKey(User,on_delete=models.PROTECT, null=True,blank=True)    
    product= models.ForeignKey(Product,on_delete=models.PROTECT)
    description = models.TextField(max_length=200)
    start_date = models.DateField()
    expiry= models.DateField(null=True,blank=True)
    sla= models.TextField(max_length=1000)
    escalation_matrix_1= models.TextField(max_length=1000)
    escalation_matrix_2= models.TextField(max_length=1000)
    escalation_matrix_3= models.TextField(max_length=1000)
    escalation_matrix_4= models.TextField(max_length=1000)
    
    def __str__(self):
        return str(self.company) + " - " +str(self.pk)