from django import forms
from .models import Ticket, Document, Call_Time, Message
from multiupload.fields import MultiFileField




class TicketForm(forms.ModelForm):
    documents = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)

    class Meta:
        model = Ticket
        fields = ('product','issue','downtime_required','contact_person', 'phone_number', 'spare_by_zaco', 'problem')
    

class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('assignee', 'priority',)


class CallTimeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [ 'ticket_call_time']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [ 'ticket_message']

class CloseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [ 'feedback']
        

class SrForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['sr_engineer']
        
class CostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [ 'feedback']
        
class ClockIn(forms.ModelForm):
    class Meta:
        model = Call_Time
        fields = [ 'clock_in']
    
# forms.py
from django import forms

class ClockOutForm(forms.ModelForm):
    class Meta:
        model = Call_Time
        fields = ['clock_out', 'update']

    documents = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)