from django.db import models
from masters.models import Company,Location

# Create your models here.

class Amc(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT)
    amc_description = models.TextField(max_length=200)
    start_date = models.DateField(null=True,blank=True)
    expiry= models.DateField(null=True,blank=True)
    sla= models.TextField(max_length=1000)
    escalation_matrix_1= models.TextField(max_length=1000, null=True,blank=True)
    escalation_matrix_2= models.TextField(max_length=1000, null=True,blank=True)
    escalation_matrix_3= models.TextField(max_length=1000, null=True,blank=True)
    escalation_matrix_4= models.TextField(max_length=1000, null=True,blank=True)
        
    def __str__(self):
        return str(self.company) + " - " +str(self.pk)
    