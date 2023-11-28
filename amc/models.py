from django.db import models
from masters.models import Company,Location
import uuid
from django.db.models import Max
from django.utils import timezone

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
    file = models.FileField(upload_to='sla/')
    uuid = models.CharField(max_length=50, unique=True, editable=False)  # Field to store the generated UUID
    
    
            
    def __str__(self):
        return str(self.company) + " - " +str(self.uuid)

    def save(self, *args, **kwargs):
        # Check if this is a new instance (not yet saved)
        if not self.id:
            # Calculate the financial year based on the start date or use the current date
            financial_year = self.start_date.year if self.start_date else timezone.now().year
            financial_year_str = f"{financial_year}-{financial_year + 1}"

            # Get the maximum counter for the given company suffix and financial year
            max_counter_qs = (
                Amc.objects.filter(
                    company=self.company,
                    uuid__startswith=f"AMC/{self.company.company_suffix}/{financial_year_str}/"
                )
            )

            # If records exist, get the maximum counter; otherwise, start from 1
            max_counter = max_counter_qs.aggregate(Max('uuid'))['uuid__max']
            counter = int(max_counter.split('/')[-1]) + 1 if max_counter else 1

            # Generate the UUID based on the specified format
            self.uuid = f"AMC/{self.company.company_suffix}/{financial_year_str}/{counter:05d}"

        super().save(*args, **kwargs)

    