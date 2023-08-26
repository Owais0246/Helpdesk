from django.shortcuts import render, redirect
from .forms import TicketForm, DocumentForm
from .models import Ticket, Document

# Create your views here.
def create_ticket(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)
        user = request.user
        

        if ticket_form.is_valid() and document_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.company = request.user.company
            for file in request.FILES.getlist('documents'):
                Document.objects.create(ticket=ticket, file=file)
            
            return redirect('ticket_list') 

    else:
        ticket_form = TicketForm()
        document_form = DocumentForm()

    return render(request, 'support/create_ticket.html', {'ticket_form': ticket_form, 'document_form': document_form})