from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TicketForm, AssignTicketForm, CallTimeForm, CloseForm
from .models import Ticket, Document
from user.models import User
import datetime
from amc.models import Amc
from masters.models import Product

def create_ticket(request):
    user = request.user
    amc = Amc.objects.filter(company = user.user_company)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            prod = request.POST.get('product')
            product = Product.objects.get(pk=prod)
            ticket = form.save(commit=False)  # Save the TicketSupport object
            ticket.company = user.user_company
            ticket.location = user.user_loc
            ticket.product = product
            ticket.save()
            for doc in request.FILES.getlist('documents'):
                ticket.documents.create(file=doc)  # Create Document objects and associate them with the ticket
            return redirect('TicketList')
    else:
        form = TicketForm()

    return render(request, 'support/create_ticket.html', {'form': form, 'user':user, 'amc':amc,})

def ticket_list(request):
    ticket = Ticket.objects.all()
    ticket_user = Ticket.objects.filter(assignee=request.user)
    ticket_active = Ticket.objects.filter(assignee=request.user).filter(status="Open")
    ticket_close = Ticket.objects.filter(assignee=request.user).filter(status="Closed")

    context = {
        'ticket': ticket, 
        'ticket_user':ticket_user,
        'ticket_active':ticket_active,
        'ticket_close':ticket_close,
  
    }
    return render(request, 'support/ticket_list.html', context)

def ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk = pk)
    ticket1 = Ticket.objects.get(pk = pk)
    assign_form = AssignTicketForm(request.POST or None, instance= ticket)
    close_form = CloseForm(request.POST or None, instance= ticket)
    eng = User.objects.filter(is_field_engineer=True)
    sr_eng = User.objects.filter(is_sr_engineer=True)
    amc= Amc.objects.get(product=ticket.product.pk)

    
    if assign_form.is_valid():
        assign = assign_form.save(commit=False)
        ticket.status = 'Open'
        assign.save()
        messages=f"Your ticket has been assigned to {ticket.assignee.first_name}"
        ticket.ticket_message.create(messages=messages, sender=request.user)
        return redirect('Ticket', pk)
    

    elif "schedule" in request.POST:
        schedule = request.POST.get("schedule")
        eng = request.POST.get("field_engineer")
        field_engineer = User.objects.get(pk=eng)
        ticket.ticket_call_time.create(schedule=schedule, ticket_id=ticket, field_engineer=field_engineer)
        messages=f"Service is sceduled on {schedule} and the engineer would be {field_engineer.first_name}"
        ticket.ticket_message.create(messages=messages, sender=request.user)
        
        return redirect('Ticket', pk)
    
    elif "sr_engineer" in request.POST:
        sr_engineer = request.POST.get("sr_engineer")
        ticket1.update(sr_engineer=sr_engineer)
    
    elif "ticket_message" in request.POST:
        message = request.POST.get("ticket_message")
        sender = request.user
        ticket.ticket_message.create(messages=message, sender=sender)
        return redirect('Ticket', pk)
    
    elif 'close' in request.POST:
        cost = request.POST.get("cost")
        amount_return = request.POST.get("amount_return")
        feedback = request.POST.get("feedback")
        status='Closed'
        closed_at = datetime.datetime.now()
        ticket1.update(cost=cost,amount_return=amount_return,feedback=feedback,status=status,closed_at=closed_at)
        ticket.ticket_message.create(messages=feedback, sender=request.user)
        return redirect('Ticket', pk)
        

    
        
    
    context = {
        'ticket': ticket, 
        'assign_form':assign_form,
        'eng':eng,
        'close_form':close_form,
        'amc':amc,
        'sr_eng':sr_eng

    }
    return render(request, 'support/ticket.html', context)


def download_file(request, file_id):
    uploaded_file = Document.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response

