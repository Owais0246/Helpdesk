"""
Django forms for ticket management.

This module contains various forms for ticket management in the Django application.

TicketForm: Form for creating or updating a ticket.
NonAmcTicketForm: Form for creating or updating a non-AMC ticket.
AssignTicketForm: Form for assigning a ticket to a user and setting its priority.
CallTimeForm: Form for updating the call time of a ticket.
MessageForm: Form for adding a message to a ticket.
CloseForm: Form for closing a ticket and providing feedback.
SrForm: Form for assigning an SR engineer to a ticket.
CostForm: Form for providing spare cost details.
ClockIn: Form for recording the clock-in time of a field engineer.
ClockOutForm: Form for recording the clock-out time of a field engineer.
SpareCostForm: Form for providing spare cost details.

"""
from django import forms
from multiupload.fields import MultiFileField
from .models import Ticket, Call_Time, SpareCost



class TicketForm(forms.ModelForm):
    """
    Form for creating or updating a ticket.
    """
    documents = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*500, required=False)

    class Meta:
        """
        Class containing metadata options for the TicketForm.

        Attributes:
            model: The model associated with the form (Ticket).
            fields: The fields of the model to include in the form.
        """

        model = Ticket
        fields = ('product','issue','downtime_required','contact_person',
                  'phone_number', 'spare_by_zaco', 'problem')
        

class NonAmcTicketForm(forms.ModelForm):
    documents = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*500, required=False)

    class Meta:
        model = Ticket
        fields = ('issue','downtime_required','location_text', 'spare_by_zaco', 'problem', 'address','sales_person','phone_number')
    

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


class SpareCostForm(forms.ModelForm):
    class Meta:
        model = SpareCost
        fields = ['type', 'part_no', 'sr_no', 'cost']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spare Type'}),
            'part_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Part Number'}),
            'sr_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'cost': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cost'}),
        }


class NonAmcTicketCusForm(forms.ModelForm):
    documents = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*500, required=False)

    class Meta:
        model = Ticket
        fields = ('issue','downtime_required','location_text', 'spare_by_zaco', 'problem', 'address','sales_person')