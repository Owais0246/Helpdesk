from django.shortcuts import render
from support.models import Ticket, Call_Time
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.db.models import Prefetch

@login_required
def dashboard(request):
    ticket_pending = None

    if request.user.is_customer_user:
        ticket_queryset = Ticket.objects.filter(company=request.user.user_company, location=request.user.user_loc)
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = ticket_queryset.filter(assignee=None, status="Pending")
      
    elif request.user.is_customer_admin:
        ticket_queryset = Ticket.objects.filter(company=request.user.user_company)
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = Ticket.objects.filter(assignee=None, status="Pending", location=request.user.user_loc)
        
    elif request.user.is_service_admin:
        ticket_queryset = Ticket.objects.all()
        ticket_active = ticket_queryset.filter(status="Open").select_related('assignee')
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = ticket_queryset.filter(assignee=None, status="Pending")
        
    elif request.user.is_service_agent:
        ticket_queryset = Ticket.objects.filter(assignee=request.user)
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        
    elif request.user.is_salesperson:
        ticket_queryset = Ticket.objects.filter(product__amc__salesperson=request.user)
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = ticket_queryset.filter(assignee=None, status="Pending")
    
    elif request.user.is_field_engineer or request.user.is_sr_engineer:
        ticket_queryset = Call_Time.objects.filter(field_engineer=request.user)
        ticket_new = Ticket.objects.filter(ticket_call_times__in=ticket_queryset).filter(status="Open")
        ticket_active = ticket_new | Ticket.objects.filter(sr_engineer=request.user, status="Open")
        ticket = ticket_new | Ticket.objects.filter(sr_engineer=request.user)
        ticket_close = Ticket.objects.filter(sr_engineer=request.user, status="Closed")
        
    elif request.user.is_superuser:
        ticket_queryset = Ticket.objects.all()
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = Ticket.objects.filter(assignee=None, status="Pending")
    
    context = {
        'ticket': ticket_queryset,
        'ticket_active': ticket_active,
        'ticket_close': ticket_close,
        'ticket_pending': ticket_pending,
    }
    
    return render(request, 'dashboard/index.html', context)
