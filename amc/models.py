from django.db import models
from masters.models import Company, Location
import uuid
from django.db.models import Max
from django.utils import timezone
from user.models import User

# Create your models here.


class Source(models.Model):
    source_name = models.CharField(max_length=100)

    def __str__(self):
        return self.source_name


class Service(models.Model):
    service_provider = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.service_provider


class Amc(models.Model):
    
    uuid = models.CharField(max_length=50, unique=True, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    amc_description = models.TextField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    expiry = models.DateField(null=True, blank=True)
    sla = models.TextField(max_length=1000)
    sla_file = models.FileField(upload_to='sla/', null=True, blank=True)
    invoice = models.FileField(upload_to='invoice/', null=True, blank=True)
    po = models.FileField(upload_to='po/', null=True, blank=True)
    log = models.FileField(upload_to='log/', null=True, blank=True)
    config = models.FileField(upload_to='config/', null=True, blank=True)
    file = models.FileField(upload_to='amc/', null=True, blank=True)
    salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    service_provider = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    escalation_matrix_1 = models.TextField(max_length=1000, null=True, blank=True)
    escalation_matrix_2 = models.TextField(max_length=1000, null=True, blank=True)
    escalation_matrix_3 = models.TextField(max_length=1000, null=True, blank=True)
    escalation_matrix_4 = models.TextField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return str(self.company) + " - " + str(self.uuid)

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
