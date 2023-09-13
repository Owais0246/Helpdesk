from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, AssignTicketForm, CallTimeForm
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

def ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk = pk)
    assign_form = AssignTicketForm(request.POST or None, instance= ticket)
    form = CallTimeForm(request.POST)
    if 'edit_blog' in request.POST:

        if assign_form.is_valid():
            assign = assign_form.save(commit=False)
            assign.status = 'Open'
            assign.save()
            return redirect('Ticket', pk)
        
        
        elif form.is_valid():
            call_time = form.save(commit=False)
            call_time.ticket = ticket
            call_time.save()
            return redirect('Ticket', pk)
        
        
    context = {
        'ticket': ticket, 
        'assign_form':assign_form,
        'form':form,
    }
    return render(request, 'support/ticket.html', context)


