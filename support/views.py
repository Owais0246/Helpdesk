from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TicketForm, AssignTicketForm, CallTimeForm, CloseForm, ClockIn, ClockOut
from .models import Ticket, Document, Call_Time, MessageDocument
from user.models import User
import datetime
from amc.models import Amc
from masters.models import Product, Company, Location
from django.http import FileResponse
import os
from django.conf import settings
from django.core.mail import send_mail
from .utils import build_absolute_url
from django.utils.safestring import mark_safe


def create_ticket(request):
    user = request.user
    company = Location.objects.filter(loc_company = user.user_company.pk)
    # amc = Amc.objects.get(company=company)
    product = Product.objects.filter(amc__company_id=user.user_company.pk)

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
                
                
            subject = f'Ticket ID {ticket.uuid} was created'
            message = f'Hi Ticket ID: {ticket.uuid}, by {ticket.company} was created. Click here to view the ticket: {build_absolute_url(request, "Ticket", pk=ticket.pk)}'
            email_from = 'info@zacocomputer.com'  # Your Gmail address from which you want to send emails
            recipient_list = ['abhiraj@zacocomputer.com', ]
            send_mail(subject, message, email_from, recipient_list)
            
            
            return redirect('/')
    else:
        form = TicketForm()

    return render(request, 'support/create_ticket.html', {'form': form, 'user':user, 'product':product,})

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
    ticket_user = User.objects.filter(user_company=ticket.company)
    admin = User.objects.filter(is_service_admin=True)
    
    admin_list = [user.email for user in admin]
    email_list = [user.email for user in ticket_user] + admin_list
    if ticket.assignee:
        email_list.append(ticket.assignee.email)
    
                # fe_list = email_list.append(call_time.get_field_engineer_email())
    
    
    ticket1 = Ticket.objects.filter(pk = pk)
    assign_form = AssignTicketForm(request.POST or None, instance= ticket)
    close_form = CloseForm(request.POST or None, instance= ticket)
    eng = User.objects.filter(is_field_engineer=True)
    sr_eng = User.objects.filter(is_sr_engineer=True)
    is_service_agent = User.objects.filter(is_service_agent=True)
    selected_product = Product.objects.get(pk=ticket.product.pk)
    amc = selected_product.amc
    call_filter = Call_Time.objects.filter(ticket_id=pk).filter(field_engineer=request.user)


    if assign_form.is_valid():
        assign = assign_form.save(commit=False)
        ticket.status = 'Open'
        assign.save()
        messages=f'''Your ticket has been assigned to {ticket.assignee.first_name} {ticket.assignee.last_name} you can contact them at
        {ticket.assignee.user_contact_no} or email at {ticket.assignee.email}
        '''
        ticket.ticket_message.create(messages=messages, sender=request.user)
        
        
        subject = f'Ticket ID {ticket.uuid} was assigned to {ticket.assignee.first_name} {ticket.assignee.last_name}'
        message = f'Hi Ticket ID: {ticket.uuid}, was assigned to {ticket.assignee.first_name} {ticket.assignee.last_name}. Click here to view the ticket: {build_absolute_url(request, "Ticket", pk=ticket.pk)}'
        email_from = 'info@zacocomputer.com'  # Your Gmail address from which you want to send emails
        recipient_list = email_list
        send_mail(subject, message, email_from, recipient_list)
        
        
        return redirect('Ticket', pk)
    

    elif "schedule" in request.POST:
        schedule = request.POST.get("schedule")
        eng = request.POST.get("field_engineer")
        # fe = User.objects.get(pk=eng)
        # fe_email_obj = fe.email
        # # print(fe_email_obj)
        # if ticket.ticket_call_time:
            
        
        field_engineer = User.objects.get(pk=eng)
        ticket.ticket_call_time.create(schedule=schedule, ticket_id=ticket, field_engineer=field_engineer)
        messages=f'''Service is scheduled on {schedule} and the engineer would be {field_engineer.first_name} {field_engineer.last_name}
        you can contact them at {field_engineer.user_contact_no} or email at {field_engineer.email}
        '''
        ticket.ticket_message.create(messages=messages, sender=request.user)
        
        messages1=f''' {field_engineer.first_name} {field_engineer.last_name} is fully vaccinated you can access the vaccine certificate and ID proof
        from schedule call section
        '''
        ticket.ticket_message.create(messages=messages1, sender=request.user)
        
        for call_time in ticket.ticket_call_time.all():
                fe_email = [call_time.get_field_engineer_email()]
                if fe_email not in email_list:
                    fe_email = email_list + fe_email
        
        subject = f'Ticket ID {ticket.uuid} service is scheduled on {schedule}'
        message = f'''Hi Ticket ID: {ticket.uuid}, Service is scheduled on {schedule} 
        and the engineer would be {field_engineer.first_name} {field_engineer.last_name}. 
        Click here to view the ticket: {build_absolute_url(request, "Ticket", pk=ticket.pk)}'''
        email_from = 'info@zacocomputer.com'  # Your Gmail address from which you want to send emails
        recipient_list = fe_email
        send_mail(subject, message, email_from, recipient_list)
        
        
        
        
        
        return redirect('Ticket', pk)
    
    
    elif "sr_engineer" in request.POST:
        sr_engineer = request.POST.get("sr_engineer")
        ticket1.update(sr_engineer=sr_engineer)
        sr_eng = User.objects.get(pk = sr_engineer)
        
    
        subject = f'Ticket ID {ticket.uuid} your assistance is required'
        message = f'''Hi Ticket ID: {ticket.uuid}, needs your assistance
        Click here to view the ticket: {build_absolute_url(request, "Ticket", pk=ticket.pk)}'''
        email_from = 'info@zacocomputer.com'  # Your Gmail address from which you want to send emails
        recipient_list = [sr_eng.email]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('Ticket', pk)
    
        
    if "ticket_message" in request.POST:
        message_text = request.POST.get("ticket_message")
        sender = request.user
        ticket_message = ticket.ticket_message.create(messages=message_text, sender=sender)

        # Handle file upload
        document = request.FILES.get("document")
        if document:
            # Save the document associated with the message
            document_instance = MessageDocument.objects.create(message=ticket_message, file=document)

            # Include a clickable link to view the document in the message
            document_link = request.build_absolute_uri(document_instance.file.url)
            clickable_link = f'<a href="{document_link}" target="_blank">here</a>'
            message_with_link = f"{message_text} New attachment received, View the document {mark_safe(clickable_link)}."
            ticket_message.messages = message_with_link
            ticket_message.sender = sender
            ticket_message.save()

        # Send email notification
        subject = f'Ticket ID {ticket.uuid} New Message'
        message = f'Hi Ticket ID: {ticket.uuid}, received new message: {message_text} from {sender.username}'
        email_from = 'info@zacocomputer.com'
        recipient_list = email_list
        send_mail(subject, message, email_from, recipient_list)

        return redirect('Ticket', pk)
    
    elif 'close' in request.POST:
        feedback = request.POST.get("feedback")
        status='Closed'
        closed_at = datetime.datetime.now()
        time = closed_at.strftime('%d/%m/%Y, %I:%M:%S %p')
        ticket1.update(feedback=feedback,status=status,closed_at=closed_at)
        ticket.ticket_message.create(messages=f''' Your ticket {ticket.uuid} has been closed at {time} here is the summary of the ticket
                                     {feedback}''', sender=request.user)
        
        subject = f'Ticket ID {ticket.uuid} was closed'
        message = f'''Hi Ticket ID: {ticket.uuid} has been closed at {time} here is the summary of the ticket {feedback}
        Click here to view the ticket: {build_absolute_url(request, "Ticket", pk=ticket.pk)}'''
        email_from = 'info@zacocomputer.com'  # Your Gmail address from which you want to send emails
        recipient_list = email_list
        send_mail(subject, message, email_from, recipient_list)
        
        
        return redirect('Ticket', pk)
    
    
    elif 'transport_cost' in request.POST:
        fe_cost = request.POST.get("fe_cost")
        spare_cost = request.POST.get("spare_cost")
        transport_cost = request.POST.get("transport_cost")
        amount_return = request.POST.get("amount_return")
        Ticket.objects.filter(pk = pk).update(fe_cost=fe_cost, spare_cost=spare_cost, transport_cost=transport_cost, amount_return=amount_return )
        return redirect('Ticket', pk)
    
    
    
    costing = 0  
    exp = 0  
    if ticket.transport_cost is not None and ticket.spare_cost is not None and ticket.fe_cost:
        costing = ticket.transport_cost + ticket.spare_cost + ticket.fe_cost
    if ticket.amount_return is not None:
        exp = costing - ticket.amount_return
    if ticket.amount_return is None:
        exp = costing
        
    
    context = {
        'ticket':ticket, 
        'assign_form':assign_form,
        'eng':eng,
        'close_form':close_form,
        'amc':amc,
        'sr_eng':sr_eng,
        'is_service_agent':is_service_agent,
        'costing':costing,
        'exp': exp,
        'call_filter':call_filter,
     

    }
    return render(request, 'support/ticket.html', context)


def show_pdf(request):
    filepath = os.path.join('static', 'sample.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def download_file(request, file_id, file_type):
    if file_type == 'document':
        file_object = Document.objects.get(pk=file_id)
        file_path = file_object.file.path
    elif file_type == 'aadhaar_no':
        user_object = User.objects.get(pk=file_id)
        file_path = user_object.aadhaar_no.path
    elif file_type == 'covid_cert':
        user_object = User.objects.get(pk=file_id)
        file_path = user_object.covid_cert.path
    else:
        # Handle invalid file types or file not found scenarios
        return HttpResponse("Invalid request", status=400)

    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
            return response
    except FileNotFoundError:
        # Handle file not found error
        return HttpResponse("File not found", status=404)
    

def clock_in(request, pk):
    call = Call_Time.objects.get(pk=pk)
    ticket = Ticket.objects.get(pk = call.ticket_id.pk)
    call_form = ClockIn(request.POST or None, instance= call)
    if call_form.is_valid():
        call_form.save()
        time = request.POST.get('clock_in')
        ticket.ticket_message.create(messages=f''' Field Engineer {call.field_engineer} has reached your location at {time}''', sender=request.user)
        return redirect('Ticket', call.ticket_id.pk)
    context = {

        'call_form':call_form,
        'call':call,
    }
    return render(request, 'support/clock_in.html', context)


def clock_out(request, pk):
    call = Call_Time.objects.get(pk=pk)
    ticket = Ticket.objects.get(pk = call.ticket_id.pk)
    call_form = ClockOut(request.POST or None, instance= call)
    if call_form.is_valid():
        call_form.save()
        time = request.POST.get('clock_out')
        update = request.POST.get('update')
        ticket.ticket_message.create(messages=f''' Field Engineer {call.field_engineer} has left your location at {time} Call Summary: {update}''', sender=request.user)
        return redirect('Ticket', call.ticket_id.pk)
    context = {

        'call_form':call_form,
        'call':call,
    }
    return render(request, 'support/clock_out.html', context)