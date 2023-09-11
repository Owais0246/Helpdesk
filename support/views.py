from django.shortcuts import render, redirect
from .forms import TicketForm
from .models import Ticket, Document

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save()  # Save the TicketSupport object
            for doc in request.FILES.getlist('documents'):
                ticket.documents.create(file=doc)  # Create Document objects and associate them with the ticket
            return redirect('ticket_list')
    else:
        form = TicketForm()

    return render(request, 'support/create_ticket.html', {'form': form})

def ticket_list(request):
    ticket = Ticket.objects.all()
    ticket_user = Ticket.objects.filter(assignee=request.user)

    context = {
        'ticket': ticket, 
        'ticket_user':ticket_user
    }
    return render(request, 'support/ticket_list.html', context)
