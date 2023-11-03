from django.db import models
from masters.models import Company, Location, Product
from user.models import User
import datetime


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
    uuid = models.CharField(max_length=200, unique=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    location_text = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    issue = models.TextField()
    documents = models.ManyToManyField("Document", blank=True)
    downtime_required = models.BooleanField(default=False)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50)
    spare_by_zaco = models.BooleanField(default=False)
    sr_engineer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ticket_call_time = models.ManyToManyField("Call_Time", blank=True)
    status = models.CharField(max_length=100, choices=Status, default='Pending')
    priority = models.CharField(max_length=100, choices=Priority, default='Mid')
    feedback = models.TextField()
    ticket_message = models.ManyToManyField("Message", blank=True)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True)
    problem = models.TextField(null=True, blank=True)
    fe_cost = models.IntegerField(null=True, blank=True)
    spare_cost = models.IntegerField(null=True, blank=True)
    transport_cost = models.IntegerField(null=True, blank=True)
    amount_return = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.issue + " - " + "ZCPL/"+str(self.pk) + " - UUID -" + str(self.uuid)
    
def generate_uuid():
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    counter = 1

    # Get the last created object
    last_obj = Ticket.objects.order_by('-created_at').first()

    if last_obj:
        # Parse the last UUID to extract the counter
        parts = last_obj.uuid.split('/')
        counter = int(parts[-1])
        # Check if the UUID is for the same date
        if int(parts[2]) == year and int(parts[3]) == month and int(parts[4]) == day:
            # If yes, increment the counter
            counter += 1
        else:
            # If not, reset the counter
            counter += 1
    else:
        # No objects exist yet, start the counter at 1
        counter += 1

    # Format the UUID
    uuid = f"ZCPL/{month:02}/{day:02}/{year}/{counter:05}"

    return uuid

# Connect the function to the model's pre-save signal
def set_uuid(sender, instance, **kwargs):
    if not instance.uuid:
        instance.uuid = generate_uuid()

models.signals.pre_save.connect(set_uuid, sender=Ticket)

class Document(models.Model):
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.file.name

class Call_Time(models.Model):
    ticket_id = models.ForeignKey('Ticket', related_name='ticket_call_times', on_delete=models.CASCADE, null=True, blank=True)
    schedule = models.DateTimeField(blank=True, null=True)
    clock_in = models.DateTimeField(blank=True, null=True)
    clock_out = models.DateTimeField(blank=True, null=True)
    update = models.TextField(blank=True, null=True)
    field_engineer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def get_field_engineer_email(self):
        if self.field_engineer:
            return self.field_engineer.email
        return None

class Message(models.Model):
    sent_on = models.DateTimeField(auto_now_add=True)
    messages = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sent_on = models.DateTimeField(auto_now=True)