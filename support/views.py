from django.shortcuts import render, redirect
from .forms import TicketForm
from .models import Ticket, Document

def create_ticket(request):
    user = request.user
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)  # Save the TicketSupport object
            ticket.company = user.user_company
            ticket.location = user.user_loc
            ticket.save()
            for doc in request.FILES.getlist('documents'):
                ticket.documents.create(file=doc)  # Create Document objects and associate them with the ticket
            return redirect('TicketList')
    else:
        form = TicketForm()

    return render(request, 'support/create_ticket.html', {'form': form, 'user':user})

def ticket_list(request):
    ticket = Ticket.objects.all()
    ticket_user = Ticket.objects.filter(assignee=request.user)

    context = {
        'ticket': ticket, 
        'ticket_user':ticket_user
    }
    return render(request, 'support/ticket_list.html', context)
