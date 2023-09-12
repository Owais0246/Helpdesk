from django.db import models
from masters.models import Company, Location, Product
from user.models import User


Status = [
        ('Pending', 'Pending'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Hold', 'Hold'),
        # Add more issue choices as needed
    ]


Priority = [
        ('High', 'High'),
        ('Mid', 'Mid'),
        ('Low', 'Low'),
        # Add more issue choices as needed
    ]

class Ticket(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    location_text = models.CharField(max_length=50, null=True, blank=True)
    product = models.CharField(max_length=50, null=True, blank=True)
    issue = models.TextField()
    documents = models.ManyToManyField("Document", blank=True)
    downtime_required = models.BooleanField(default=False)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50)
    spare_by_zaco = models.BooleanField(default=False)
    sr_engineer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ticket_call_time = models.ManyToManyField("Call_Time", blank=True)
    cost = models.CharField(max_length=150)
    amount_return = models.CharField( max_length=150)
    status = models.CharField(max_length=100, choices=Status, default='Pending')
    priority = models.CharField(max_length=100, choices=Priority, default='Mid')
    feedback = models.TextField()
    ticket_message = models.ManyToManyField("Message", blank=True)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField()
    
    def __str__(self):
        return self.product

class Document(models.Model):
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.file.name

class Call_Time(models.Model):
    schedule = models.DateTimeField(blank=True, null=True)
    clock_in = models.DateTimeField(blank=True, null=True)
    clock_out = models.DateTimeField(blank=True, null=True)
    update = models.TextField()
    field_engineer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Message(models.Model):
    sent_on = models.DateTimeField(auto_now_add=True)
    messages = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sent_on = models.DateTimeField(auto_now=True)