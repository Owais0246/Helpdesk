"""
Module: views.py
Description: This module contains views for handling AMC 
(Annual Maintenance Contract) reports and details.
"""
import datetime
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.utils.timezone import now
from user.models import User
from amc.models import Amc
from support.models import Ticket
from masters.models import Product, Company



def amc_list(request):
    """
    View function to render a list of AMC reports based on various filters.

    Parameters:
    - request: HttpRequest object

    Returns:
    - HttpResponse object containing the rendered HTML template with AMC reports list
    """

    queryset = Amc.objects.all()  # pylint: disable=E1101

    # Apply filters based on request parameters
    active = request.GET.get('active')
    client_name = request.GET.get('client_name')
    sales_person = request.GET.get('sales_person')
    amc_start_date = request.GET.get('amc_start_date')
    amc_end_date = request.GET.get('amc_end_date')
    location = request.GET.get('location')

    if active:
        queryset = queryset.filter(active=active)
    if client_name:
        queryset = queryset.filter(company__id=client_name)
    if sales_person:
        queryset = queryset.filter(salesperson__id=sales_person)
    if amc_start_date:
        queryset = queryset.filter(start_date__gte=amc_start_date)
    if amc_end_date:
        queryset = queryset.filter(expiry__lte=amc_end_date)
    if location:
        queryset = queryset.filter(salesperson__user_loc__loc_name=location)

    # Calculate margin and ticket counts for each AMC instance
    for amc in queryset:
        total_expenses = 0
        amount_return = 0
        total_product_amount = amc.products.aggregate(Sum('amount'))['amount__sum'] or 0
        tickets = Ticket.objects.filter(product__amc=amc)  # pylint: disable=E1101
        active_tickets_count = tickets.all().count()
        inactive_tickets_count = tickets.filter(status='Closed').count()
        for ticket in tickets:
            total_expenses += ticket.fe_cost or 0
            amount_return += ticket.amount_return or 0
            total_expenses += ticket.transport_cost or 0
            spare_costs = ticket.spare_cost.aggregate(Sum('cost'))['cost__sum'] or 0
            total_expenses += spare_costs
        amc.margin_earned_amt = total_product_amount - total_expenses + amount_return
        amc.margin_earned_percent = (
            amc.margin_earned_amt / total_product_amount) * 100 if total_product_amount != 0 else 0
        amc.total_expenses = total_expenses
        amc.po_value = total_product_amount
        amc.amount_return = amount_return
        amc.active_tickets_count = active_tickets_count
        amc.inactive_tickets_count = inactive_tickets_count
        amc.is_expired = amc.expiry < now().date()

    salespersons = User.objects.filter(is_salesperson=True)  # pylint: disable=E1101
    clients = Company.objects.filter(is_customer=True)  # pylint: disable=E1101
    locations = Amc.objects.values_list('salesperson__user_loc__loc_name', flat=True).distinct() # pylint: disable=E1101

    return render(request, 'reports/amc_report.html', {
        'amc_list': queryset,
        'salespersons': salespersons,
        'clients': clients,
        'locations': locations,
        'active': active,
        'client_name': client_name,
        'sales_person': sales_person,
        'amc_start_date': amc_start_date,
        'amc_end_date': amc_end_date,
        'location': location,
    })

def amc_detail(request, amc_id):
    """
    View function to render details of a specific AMC.

    Parameters:
    - request: HttpRequest object
    - amc_id: ID of the AMC instance

    Returns:
    - HttpResponse object containing the rendered HTML template with AMC details
    """

    amc = get_object_or_404(Amc, pk=amc_id)
    products = Product.objects.filter(amc=amc) # pylint: disable=E1101
    tickets = Ticket.objects.filter(product__in=products) # pylint: disable=E1101

    total_product_amount = products.aggregate(Sum('amount'))['amount__sum'] or 0
    product_count = products.count()

    for product in products:
        product_tickets = tickets.filter(product=product)
        product.ticket_count = product_tickets.count()
        product.fe_cost = product_tickets.aggregate(Sum('fe_cost'))['fe_cost__sum'] or 0
        product.spare_cost = product_tickets.aggregate(
            Sum('spare_cost__cost'))['spare_cost__cost__sum'] or 0
        product.transport_cost = product_tickets.aggregate(
            Sum('transport_cost'))['transport_cost__sum'] or 0
        product.amount_return = product_tickets.aggregate(
            Sum('amount_return'))['amount_return__sum'] or 0
        product.margin = product.amount - (
            product.fe_cost + product.spare_cost + product.transport_cost) + product.amount_return
        product.margin_percentage = (product.margin / product.amount) * 100 if product.amount else 0

    for ticket in tickets:
        ticket.call_count = ticket.ticket_call_times.count()

    is_expired = amc.expiry and amc.expiry < datetime.date.today()

    return render(request, 'reports/amc_detail.html', {
        'amc': amc,
        'products': products,
        'tickets': tickets,
        'total_product_amount': total_product_amount,
        'product_count': product_count,
        'is_expired': is_expired,
    })
