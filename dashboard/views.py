"""
Views for the dashboard app.

This module contains views for the dashboard app, including the main dashboard view.

Functions:
    dashboard: View function for rendering the dashboard page, 
    displaying ticket information based on user roles.

"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from support.models import Ticket, Call_Time

@login_required
def dashboard(request):
    """
    Render the dashboard page.

    This view function renders the dashboard page, 
    displaying ticket information based on the user's role:
    - For customer users: Display tickets related to their company and location.
    - For customer admins: Display tickets related to their company and all locations.
    - For service admins: Display all tickets with assigned agents.
    - For service agents: Display tickets assigned to them.
    - For salespersons: Display tickets related to products they are responsible for.
    - For field engineers or senior engineers: Display tickets assigned to them or 
        open for their intervention.
    - For superusers: Display all tickets.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object rendering the dashboard page.

    """
    ticket_pending = None

    if request.user.is_customer_user:
        ticket_queryset = Ticket.objects.filter(company=request.user.user_company, location=request.user.user_loc) # pylint: disable=no-member line-too-long
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = ticket_queryset.filter(assignee=None, status="Pending")

    elif request.user.is_customer_admin:
        ticket_queryset = Ticket.objects.filter(company=request.user.user_company) # pylint: disable=no-member
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = Ticket.objects.filter(assignee=None, status="Pending", location=request.user.user_loc) # pylint: disable=no-member line-too-long

    elif request.user.is_service_admin:
        ticket_queryset = Ticket.objects.all() # pylint: disable=no-member
        ticket_active = ticket_queryset.filter(status="Open").select_related('assignee')
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = ticket_queryset.filter(assignee=None, status="Pending")

    elif request.user.is_service_agent:
        ticket_queryset = Ticket.objects.filter(assignee=request.user) # pylint: disable=no-member
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")

    elif request.user.is_salesperson:
        ticket_queryset = Ticket.objects.filter(product__amc__salesperson=request.user) # pylint: disable=no-member
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = ticket_queryset.filter(assignee=None, status="Pending")

    elif request.user.is_field_engineer or request.user.is_sr_engineer:
        ticket_queryset = Call_Time.objects.filter(field_engineer=request.user) # pylint: disable=no-member
        ticket_new = Ticket.objects.filter(ticket_call_times__in=ticket_queryset).filter(status="Open") # pylint: disable=no-member line-too-long
        ticket_active = ticket_new | Ticket.objects.filter(sr_engineer=request.user, status="Open") # pylint: disable=no-member
        # ticket = ticket_new | Ticket.objects.filter(sr_engineer=request.user) # pylint: disable=no-member
        ticket_close = Ticket.objects.filter(sr_engineer=request.user, status="Closed") # pylint: disable=no-member

    elif request.user.is_superuser:
        ticket_queryset = Ticket.objects.all() # pylint: disable=no-member
        ticket_active = ticket_queryset.filter(status="Open")
        ticket_close = ticket_queryset.filter(status="Closed")
        ticket_pending = Ticket.objects.filter(assignee=None, status="Pending") # pylint: disable=no-member

    context = {
        'ticket': ticket_queryset,
        'ticket_active': ticket_active,
        'ticket_close': ticket_close,
        'ticket_pending': ticket_pending,
    }

    return render(request, 'dashboard/index.html', context)
