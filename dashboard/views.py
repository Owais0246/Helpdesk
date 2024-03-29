from django.shortcuts import render
from support.models import Ticket, Call_Time
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def dashboard(request):
    ticket_pending={}

    if request.user.is_customer_user == True:
        ticket = Ticket.objects.filter(company = request.user.user_company).filter(location=request.user.user_loc)
        ticket_active = Ticket.objects.filter(company = request.user.user_company).filter(status="Open").filter(location=request.user.user_loc)
        ticket_close = Ticket.objects.filter(company = request.user.user_company).filter(status="Closed").filter(location=request.user.user_loc)
        ticket_pending = Ticket.objects.filter(assignee=None).filter(status="Pending").filter(location=request.user.user_loc)
      
    if request.user.is_customer_admin == True:
        ticket = Ticket.objects.filter(company = request.user.user_company)
        ticket_active = Ticket.objects.filter(company = request.user.user_company).filter(status="Open")
        ticket_close = Ticket.objects.filter(company = request.user.user_company).filter(status="Closed")
        ticket_pending = Ticket.objects.filter(assignee=None).filter(status="Pending").filter(location=request.user.user_loc)
        
    elif request.user.is_service_admin == True:
        ticket = Ticket.objects.all()
        ticket_active = Ticket.objects.filter(assignee=request.user).filter(status="Open")
        ticket_close = Ticket.objects.filter(status="Closed")
        ticket_pending = Ticket.objects.filter(assignee=None).filter(status="Pending")
        
    elif request.user.is_service_agent == True:
        ticket = Ticket.objects.filter(assignee=request.user)
        ticket_active = Ticket.objects.filter(assignee=request.user).filter(status="Open")
        ticket_close = Ticket.objects.filter(assignee=request.user).filter(status="Closed")
        
    elif request.user.is_salesperson == True:
        ticket = Ticket.objects.filter(product__amc__salesperson=request.user)
        ticket_active = Ticket.objects.filter(product__amc__salesperson=request.user).filter(status="Open")
        ticket_close = Ticket.objects.filter(product__amc__salesperson=request.user).filter(status="Closed")
        ticket_pending = Ticket.objects.filter(product__amc__salesperson=request.user).filter(assignee=None).filter(status="Pending")
        
    
    elif request.user.is_field_engineer == True or request.user.is_sr_engineer == True:
        call_times = Call_Time.objects.filter(field_engineer=request.user)
        call_times_active = Call_Time.objects.filter(field_engineer=request.user, clock_out__isnull=True)
        ticket_new = Ticket.objects.filter(ticket_call_times__in=call_times_active)
        ticket_active = ticket_new.filter(status="Open") | Ticket.objects.filter(sr_engineer=request.user).filter(status="Open")
        ticket_active = ticket_active.distinct()
        ticket_active1 = ticket_new.filter(status="Open") or Ticket.objects.filter(sr_engineer=request.user).filter(status="Open")
        ticket = ticket_active1 | Ticket.objects.filter(sr_engineer=request.user)
        ticket = ticket.distinct()
        ticket_close = None or Ticket.objects.filter(sr_engineer=request.user).filter(status="Closed")
        
    elif request.user.is_superuser == True:
        ticket = Ticket.objects.all()
        ticket_active = Ticket.objects.all()
        ticket_close = Ticket.objects.all()
        ticket_pending = Ticket.objects.filter(assignee=None).filter(status="Pending")
    
        
        
    context = {
        'ticket': ticket,
        'ticket_active':ticket_active,
        'ticket_close':ticket_close,
        'ticket_pending': ticket_pending
  
    }
    # return render(request, 'support/ticket_list.html', context)
    
    return render(request,'dashboard/index.html', context)