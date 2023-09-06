from django import forms
from .models import Ticket, Document, Call_Time, Message
from multiupload.fields import MultiFileField




class TicketForm(forms.ModelForm):
    documents = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)

    class Meta:
        model = Ticket
        fields = ('product','issue','downtime_required','contact_person', 'phone_number', 'spare_by_zaco')
    
