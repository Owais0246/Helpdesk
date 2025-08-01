from threading import Thread
import os
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from user.models import User
from masters.models import Product, Location, Company
from .models import Ticket, Document, Call_Time, MessageDocument, CallDocument
from .forms import TicketForm, AssignTicketForm, CloseForm, ClockIn, ClockOutForm, NonAmcTicketForm, NonAmcTicketCusForm
from .utils import build_absolute_url
from django.utils.safestring import mark_safe
from threading import Thread
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import formset_factory
from .forms import SpareCostForm
from masters.forms import CompanyForm, ProductForm
from user.forms import CreateUserNew
from django.urls import reverse
from django.http import HttpRequest
def build_subdomain_absolute_uri(request: HttpRequest, view_name: str, *args, **kwargs) -> str:
    # Define the subdomain
    subdomain = "itservicedesk"  # Replace "itservicedesk" with your desired subdomain

    # Get the current scheme (http or https)
    scheme = "https" if request.is_secure() else "http"

    # Build the absolute URL using the reverse function
    path = reverse(view_name, args=args, kwargs=kwargs)
    domain = f"{subdomain}.zacocomputer.com"  # Set the correct domain here
    return f"{scheme}://{domain}{path}"

def send_email_async(subject, message, email_from, recipient_list):
    """
    A function to send emails asynchronously using threading.
    """
    send_mail(subject, message, email_from, recipient_list)


@login_required
def create_ticket(request):
    user = request.user
    admin = User.objects.filter(is_service_admin=True)
    admin_email = [x.email for x in admin]
    

    company = Location.objects.filter(loc_company=user.user_company.pk)
    # amc = Amc.objects.get(company=company)

    product = Product.objects.filter(amc__company_id=user.user_company.pk).filter(
        location=user.user_loc
    )

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            prod = request.POST.get("product")
            product = Product.objects.get(pk=prod)
            ticket = form.save(commit=False)  # Save the TicketSupport object
            ticket.company = user.user_company
            ticket.location = user.user_loc
            ticket.product = product
            ticket.raised_by = user
            ticket.sales_person = ticket.product.amc.salesperson
            ticket.save()
            for doc in request.FILES.getlist('documents'):
                ticket.documents.create(file=doc)  # Create Document objects and associate them with the ticket


            sales_person = [ticket.product.amc.salesperson.email]
            email_template_path = "email/ticket_create_mail.html"
            build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk)
            ticket_link = build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk)
            email_content = render_to_string(
                email_template_path,
                {
                    "ticket": ticket,
                    "ticket_link": ticket_link,
                },
            )
            subject = f" New Ticket Created - Ticket ID: {ticket.uuid}"
            message = email_content
            email_from = 'info@zacocomputer.com'
            recipient_list = [ticket.raised_by.email]+admin_email+sales_person
                    
            email_thread = Thread(target=send_email_async, args=(subject, message, email_from, recipient_list))
            email_thread.start()

            return redirect("/")
    else:
        form = TicketForm()

    return render(
        request,
        "support/create_ticket.html",
        {
            "form": form,
            "user": user,
            "product": product,
        },
    )


@login_required
def ticket_list(request):
    # Redirect customer users or customer admins to the dashboard
    if request.user.is_customer_user or request.user.is_customer_admin:
        return redirect('dashboard')

    ticket = Ticket.objects.all()
    ticket_user = Ticket.objects.filter(assignee=request.user)
    ticket_active = Ticket.objects.filter(assignee=request.user, status="Open")
    ticket_close = Ticket.objects.filter(assignee=request.user, status="Closed")

    context = {
        "ticket": ticket,
        "ticket_user": ticket_user,
        "ticket_active": ticket_active,
        "ticket_close": ticket_close,
    }
    return render(request, "support/ticket_list.html", context)

@login_required
def ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    admin = User.objects.filter(is_service_admin=True)
    ticket1 = Ticket.objects.filter(pk=pk)
    assign_form = AssignTicketForm(request.POST or None, instance=ticket)
    close_form = CloseForm(request.POST or None, instance=ticket)
    eng = User.objects.filter(is_field_engineer=True) | User.objects.filter(
        is_sr_engineer=True
    )
    sr_eng = User.objects.filter(is_sr_engineer=True)
    is_service_agent = User.objects.filter(
        is_service_agent=True
    ) or User.objects.filter(is_service_admin=True)
    selected_product = Product.objects.get(pk=ticket.product.pk)
    amc = selected_product.amc
    call_filter = Call_Time.objects.filter(ticket_id=pk).filter(field_engineer=request.user)
    SpareCostFormSet = formset_factory(SpareCostForm, extra=1)
    sender = request.user

    if ticket.assignee is not None:
        assign_email = ticket.assignee.email

    if assign_form.is_valid():
        assign = assign_form.save(commit=False)
        assign.status = "Open"
        assign.save()

        messages = f"""Your ticket has been assigned to {ticket.assignee.first_name} {ticket.assignee.last_name}. 
        You can contact them at {ticket.assignee.user_contact_no} or email at {ticket.assignee.email} for further assistance.
        """
        ticket.ticket_message.create(messages=messages, sender=request.user)

        email_template_path = "email/ticket_assign_mail.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
            },
        )

        subject = f"""Ticket Assignment Confirmation - Ticket ID: {ticket.uuid}"""
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [ticket.assignee.email, ticket.raised_by.email]
        # print(recipient_list)
        email_thread = Thread(target=send_email_async, args=(subject, message, email_from, recipient_list))
        email_thread.start()

        return redirect("Ticket", pk)

    elif "schedule" in request.POST:
        schedule = request.POST.get("schedule")
        eng = request.POST.get("field_engineer")
        # fe = User.objects.get(pk=eng)
        # fe_email_obj = fe.email
        # # print(fe_email_obj)
        # if ticket.ticket_call_time:

        field_engineer = User.objects.get(pk=eng)
        ticket.ticket_call_time.create(
            schedule=schedule, ticket_id=ticket, field_engineer=field_engineer
        )
        messages = f"""Your service is scheduled on {schedule}, and the assigned engineer is {field_engineer.first_name} {field_engineer.last_name}. 
        You can contact them at {field_engineer.user_contact_no} or email at {field_engineer.email} for any inquiries or assistance.
        """
        ticket.ticket_message.create(messages=messages, sender=request.user)

        messages1 = f"""We're pleased to inform you that {field_engineer.first_name} {field_engineer.last_name} is fully vaccinated. You can access the vaccine certificate and ID proof from the Schedule Call section.
        """
        ticket.ticket_message.create(messages=messages1, sender=request.user)

        # for call_time in ticket.ticket_call_time.all():
        #         fe_email = [call_time.get_field_engineer_email()]
        #         if fe_email not in email_list:
        #             fe_email = email_list + fe_email

        email_template_path = "email/ticket_schedule_mail.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
                "field_engineer": field_engineer,
                "schedule": schedule,
            },
        )

        subject = f"Service Schedule and Engineer Assigned  - Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [field_engineer.email, ticket.raised_by.email]
        # print(recipient_list)
        
        email_thread = Thread(target=send_email_async, args=(subject, message, email_from, recipient_list))
        email_thread.start()

        return redirect("Ticket", pk)

    elif "sr_engineer" in request.POST:
        sr_engineer = request.POST.get("sr_engineer")
        ticket1.update(sr_engineer=sr_engineer)
        sr_eng = User.objects.get(pk=sr_engineer)

        email_template_path = "email/ticket_sr_mail.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
            },
        )
        subject = f"Urgent Assistance Needed - Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [sr_eng.email]

        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
        email_thread.start()
        # print(assign_email)
        return redirect('Ticket', pk)
    
      
    elif "ticket_message" in request.POST:
        message_text = request.POST.get("ticket_message")

        # Create the initial ticket_message without attachments
        if len(message_text) > 1:
            ticket_message = ticket.ticket_message.create(
                messages=message_text, sender=sender
            )

        # Handle file upload
        documents = request.FILES.getlist("document")

        ticket_messages = []

        for document in documents:
            # Create a new ticket_message for each file
            ticket_message_with_attachment = ticket.ticket_message.create(sender=sender)

            # Save the document associated with the message
            document_instance = MessageDocument.objects.create(
                message=ticket_message_with_attachment, file=document
            )

            # Include a clickable link to view the document in the message
            document_link = request.build_absolute_uri(document_instance.file.url)
            clickable_link = (
                f'<a href="{document_link}" target="_blank">{document.name}</a>'
            )
            message_with_link = f" New attachment received, View the document {mark_safe(clickable_link)}."

            # Update the ticket_message with the message containing the attachment
            ticket_message_with_attachment.messages = message_with_link
            ticket_message_with_attachment.save()

            ticket_messages.append(ticket_message_with_attachment)

        email_template_path = "email/ticket_message_mail.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
            },
        )
        subject = f"Ticket ID {ticket.uuid} New Message"
        message = email_content
        email_from = "info@zacocomputer.com"
        recipient_list = [assign_email, ticket.raised_by.email]
        
        if sender.email in recipient_list:
            recipient_list.remove(sender.email)
        # print(recipient_list)

        # Use threading to send the email asynchronously
        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
        email_thread.start()

        return redirect('Ticket', pk)
    elif 'close' in request.POST:
            feedback = request.POST.get("feedback")
            status='Closed'
            closed_at = datetime.datetime.now()
            time = closed_at.strftime('%d/%m/%Y, %I:%M:%S %p')
            ticket1.update(feedback=feedback,status=status,closed_at=closed_at)
            ticket.ticket_message.create(messages=f'''Your ticket {ticket.uuid} has been successfully closed at {time}. Here is a summary of the ticket:
                                                    {feedback}
                                                    If you have any further questions or need assistance, feel free to reach out.''', sender=request.user)
            
            
            email_template_path = "email/ticket_close_email.html"
            email_content = render_to_string(email_template_path, {'ticket': ticket, 
                                                                'ticket_link': build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
                                                                'time':time,
                                                                'feedback':feedback,
                                                                })
            
            subject = f'Ticket Closure Notification - Ticket ID: {ticket.uuid}'
            message = email_content
            if ticket.product.amc is None:
                sales_person = ticket.sales_person.email
            else:
                sales_person = ticket.product.amc.salesperson.email
                
            email_from = 'info@zacocomputer.com'  # Your Gmail address from which you want to send emails
            recipient_list = [assign_email, ticket.raised_by.email, sales_person]
            if sender.email in recipient_list:
                recipient_list.remove(sender.email)
            print(recipient_list)
            
            email_thread = Thread(target=send_email_async, args=(subject, message, email_from, recipient_list))
            email_thread.start()
            
            
            print(recipient_list)
            
            return redirect('Ticket', pk)
    
    elif 'transport_cost' in request.POST:
        fe_cost = request.POST.get("fe_cost")
        transport_cost = request.POST.get("transport_cost")
        amount_return = request.POST.get("amount_return")

        # Update the Ticket model
        ticket = Ticket.objects.get(pk=pk)
        ticket.fe_cost = fe_cost
        ticket.transport_cost = transport_cost
        ticket.amount_return = amount_return
        ticket.save()

        # Process Spare Cost Formset
        SpareCostFormSet = formset_factory(SpareCostForm, extra=1)
        spare_cost_formset = SpareCostFormSet(request.POST, prefix='spare_cost')

        # Check if the formset is valid
        if spare_cost_formset.is_valid():
            # Iterate through the forms in the formset and create SpareCost instances
            for spare_cost_form in spare_cost_formset:
                if spare_cost_form.is_valid():
                    spare_cost = spare_cost_form.save(commit=False)
                    spare_cost.ticket = ticket
                    spare_cost.save()

                    # Add the SpareCost instance to the many-to-many relationship
                    ticket.spare_cost.add(spare_cost)

            # Calculate costing and exp


            # if ticket.transport_cost is not None and ticket.fe_cost:
            #     costing = ticket.transport_cost + ticket.fe_cost

            # if ticket.amount_return is not None:
            #     exp = costing - ticket.amount_return

            # if ticket.amount_return is None:
            #     exp = costing
            return redirect('Ticket', pk)
    costing = 0
    exp = 0

    if ticket.transport_cost is not None and ticket.fe_cost:
        costing += ticket.transport_cost + ticket.fe_cost

    # Add the cost from SpareCost instances only if they are associated with the ticket
    for spare_cost_instance in ticket.spare_cost.all():
        if spare_cost_instance.ticket == ticket:
            costing += spare_cost_instance.cost

    if ticket.amount_return is not None:
        exp = costing - ticket.amount_return

    if ticket.amount_return is None:
        exp = costing
    context = {
        "ticket": ticket,
        "assign_form": assign_form,
        "eng": eng,
        "close_form": close_form,
        "amc": amc,
        "sr_eng": sr_eng,
        "is_service_agent": is_service_agent,
        "costing": costing,
        "exp": exp,
        "call_filter": call_filter,
    }
    context['spare_cost_formset'] = SpareCostFormSet(prefix='spare_cost')

    return render(request, 'support/ticket.html', context)

@login_required
def show_pdf(request):
    filepath = os.path.join("static", "sample.pdf")
    return FileResponse(open(filepath, "rb"), content_type="application/pdf")


@login_required
def download_file(request, file_id, file_type):
    if file_type == "document":
        file_object = Document.objects.get(pk=file_id)
        file_path = file_object.file.path
    elif file_type == "aadhaar_no":
        user_object = User.objects.get(pk=file_id)
        file_path = user_object.aadhaar_no.path
    elif file_type == "covid_cert":
        user_object = User.objects.get(pk=file_id)
        file_path = user_object.covid_cert.path
    else:
        # Handle invalid file types or file not found scenarios
        return HttpResponse("Invalid request", status=400)

    try:
        with open(file_path, "rb") as file:
            response = HttpResponse(
                file.read(), content_type="application/force-download"
            )
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{file_path.split("/")[-1]}"'
            return response
    except FileNotFoundError:
        # Handle file not found error
        return HttpResponse("File not found", status=404)


@login_required
def clock_in(request, pk):
    call = Call_Time.objects.get(pk=pk)
    ticket = Ticket.objects.get(pk=call.ticket_id.pk)
    call_form = ClockIn(request.POST or None, instance=call)
    assign_email = ticket.assignee.email
    if call_form.is_valid():
        call_form.save()
        time = request.POST.get("clock_in")
        ticket.ticket_message.create(
            messages=f""" Field Engineer {call.field_engineer.first_name} {call.field_engineer.last_name} has arrived at your location at {time}. 
                                     If you have any specific instructions or need assistance, please feel free to reach out.""",
            sender=request.user,
        )

        email_template_path = "email/ticket_clock_in_mail.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
                "time": time,
                "call": call,
            },
        )

        subject = f"Field Engineer Arrival Notification - Service for Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [assign_email, ticket.raised_by.email]


        
        # print(recipient_list)
        # print(ticket.raised_by.email)
        print(recipient_list)
        email_thread = Thread(target=send_email_async, args=(subject, message, email_from, recipient_list))
        email_thread.start()

        return redirect("Ticket", call.ticket_id.pk)
    context = {
        "call_form": call_form,
        "call": call,
    }

    return render(request, "support/clock_in.html", context)


@login_required
def clock_out(request, pk):
    call = Call_Time.objects.get(pk=pk)
    ticket = Ticket.objects.get(pk=call.ticket_id.pk)
    call_form = ClockOutForm(request.POST or None, instance=call)
    assign_email = ticket.assignee.email
    if call_form.is_valid():
        call_form.save()
        files = request.FILES.getlist("documents")
        for file in files:
            CallDocument.objects.create(call_time=call, file=file)
        time = request.POST.get("clock_out")
        update = request.POST.get("update")
        ticket.ticket_message.create(
            messages=f"""Field Engineer {call.field_engineer.first_name} {call.field_engineer.last_name} has left your location at {time}. 
                                                Here is a summary of the call update: {update}.
                                                If you have any further questions or require assistance, feel free to contact us.""",
            sender=request.user,
        )

        email_template_path = "email/ticket_clock_out_mail.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_subdomain_absolute_uri(request, "Ticket", pk=ticket.pk),
                "time": time,
                "call": call,
                "update": update,
            },
        )

        subject = f"Field Engineer Departure Notification - Service Summary for Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [assign_email, ticket.raised_by.email]

        print(recipient_list)
        
        email_thread = Thread(target=send_email_async, args=(subject, message, email_from, recipient_list))
        email_thread.start()
        print(recipient_list)

        return redirect("Ticket", call.ticket_id.pk)
    context = {
        "call_form": call_form,
        "call": call,
    }
    return render(request, "support/clock_out.html", context)


@login_required
def view_attachment(request, attachment_id):
    attachment = get_object_or_404(CallDocument, pk=attachment_id)

    # Serve the file
    response = HttpResponse(attachment.file, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="{attachment.file.name}"'
    return response

def get_spare_cost_form(request):
    #  from .forms import SpareCostForm

    # Create an instance of the SpareCostForm
    spare_cost_form = SpareCostForm()
    return render(request, 'support/spare_cost_form_template.html', {'spare_cost_form': spare_cost_form})


def get_raised_by_details(request):
    raised_by_username = request.GET.get('raised_by_username', None)
    if raised_by_username:
        raised_by_user = get_object_or_404(User, username=raised_by_username)
        # Construct data dictionary with raised by user details
        data = {
            # Add raised by user details here
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Raised by username not provided'}, status=400)
    
    
def generate_ticket(request):
    saleuser = User.objects.filter(is_salesperson = True)
    ticket = NonAmcTicketForm(request.POST) 
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        customer_form = CompanyForm(request.POST)
        user_form = CreateUserNew(request.POST)
               

        if customer_form.is_valid() and product_form.is_valid() and user_form.is_valid() and ticket.is_valid():
            company_name = customer_form.cleaned_data['company_name']  # Adjust this based on your form field
            company_contact_no = customer_form.cleaned_data['company_contact_no']  # Adjust this based on your form field
            address = customer_form.cleaned_data['address']  # Adjust this based on your form field

            # Check if a record with the same data already exists
            existing_company = Company.objects.filter(
                company_name=company_name,
            ).first()

            if existing_company:
                # Update the existing record
                existing_company.company_contact_no = company_contact_no
                existing_company.address = address
                existing_company.is_customer = True
                existing_company.save()
            else:
                # Create a new record
                existing_company = customer_form.save(commit=False)
                existing_company.is_customer = True
                existing_company.save()
            
            product_name = product_form.cleaned_data['product_name']
            serial_number = product_form.cleaned_data['serial_number']
            model_number = product_form.cleaned_data['model_number']
            description = product_form.cleaned_data['description']
            existing_product = Product.objects.filter(
                serial_number=serial_number,
            ).first()
            if existing_product:
                # Update the existing record
                existing_product.product_name = product_name
                existing_product.serial_number = serial_number
                existing_product.model_number = model_number
                existing_product.description = description
                existing_product.save()
                
            else:
                # Create a new record
                existing_product = product_form.save(commit=False)
                existing_product.save()
            
            
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            username = email
            user_contact_no = user_form.cleaned_data['user_contact_no']
            is_customer_user = True
            password = first_name + last_name + '@2023'

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                # Update the existing user record
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.email = email
                existing_user.user_contact_no = user_contact_no
                existing_user.save()
                is_new_customer = False
            else:
                # Create a new user record
                existing_user = user_form.save(commit=False)
                existing_user.is_customer_user = True
                existing_user.set_password(password)
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.email = email
                existing_user.username = username
                existing_user.user_contact_no = user_contact_no
                existing_user.user_company = existing_company
                existing_user.save()
                is_new_customer = True
                
            location = ticket.cleaned_data['location_text']
            issue = ticket.cleaned_data['issue']
            downtime_required = ticket.cleaned_data['downtime_required']
            spare_by_zaco = ticket.cleaned_data['spare_by_zaco']
            problem = ticket.cleaned_data['problem']
            address = ticket.cleaned_data['address']
            sales_person = ticket.cleaned_data['sales_person']
            # print(location,issue,downtime_required,spare_by_zaco,problem,address,sales_person)
            ticket1 = ticket.save(commit=False)
            ticket1.raised_by = existing_user
            ticket1.phone_number = user_contact_no
            ticket1.company = existing_company
            ticket1.location_text = location
            ticket1.product = existing_product
            ticket1.contact_person = existing_user
            ticket1.issue = issue
            ticket1.problem = problem
            ticket1.downtime_required = downtime_required
            ticket1.spare_by_zaco = spare_by_zaco
            ticket1.sales_person = sales_person
            ticket1.save()
            print("Ticket Form Errors:", ticket.errors)
            
            customer_email = existing_user.email
            salesperson_id = request.POST.get('sales_person')
            selected_salesperson = User.objects.filter(pk=salesperson_id).first()
            salesperson_email = selected_salesperson.email if selected_salesperson else None
            
            # Prepare HTML message
            if is_new_customer:
                email_template_path = "email/ticket_create_mai_non_amc.html"
            else:
                email_template_path = "email/ticket_create_mail.html"
                

            ticket_link = build_subdomain_absolute_uri(request, "Ticket", pk=ticket1.pk)
            email_content = render_to_string(
                email_template_path,
                {
                    "ticket": ticket1,
                    "ticket_link": ticket_link,
                    'is_new_customer': is_new_customer,
                    "username":existing_user.username,
                    "password":password
                },
            )
            
            email_template_path_sale = "email/ticket_create_mail.html"
            email_content_sale = render_to_string(
                email_template_path_sale,
                {
                    "ticket": ticket1,
                    "ticket_link": ticket_link,
                },
            )
            
            
            subject = f" New Ticket Created - Ticket ID: {ticket1.uuid}"
            message = email_content
            messagesale = email_content_sale
            email_from = 'info@zacocomputer.com'
            recipient_list = [customer_email, salesperson_email]
            
            # For sending email to customer
            email_thread = Thread(target=send_email_async, args=(subject, message, email_from, [customer_email]))
            email_thread.start()

            # For sending email to salesperson
            email_thread = Thread(target=send_email_async, args=(subject, messagesale, email_from, [salesperson_email]))
            email_thread.start()

            return redirect('dashboard')
        else:
            print("Form errors:")
            print("Customer Form Errors:", customer_form.errors)
            print("Product Form Errors:", product_form.errors)
            print("User Form Errors:", user_form.errors)
            print("Ticket Form Errors:", ticket.errors)
    else:
        # If it's a GET request, create empty forms
        customer_form = CompanyForm()
        product_form = ProductForm()
        user_form = CreateUserNew()

    company = Company.objects.all()
    products = Product.objects.all()
    user = User.objects.filter(is_customer_user=True)

    context = {
        'customer_form': customer_form,
        'company': company,
        'products': products,
        'product_form': product_form,
        'user': user,
        'user_form': user_form,
        'saleuser':saleuser,
        'ticket':ticket
    }
    return render(request, 'support/non-amc.html', context)


def generate_ticket_cus(request):
    saleuser = User.objects.filter(is_salesperson=True)
    ticket = NonAmcTicketForm(request.POST)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        
        if product_form.is_valid() and ticket.is_valid():
            # Retrieve the company and contact number of the logged-in user
            existing_company = request.user.user_company
            user_contact_no = request.user.user_contact_no
            
            # Product details
            product_name = product_form.cleaned_data['product_name']
            serial_number = product_form.cleaned_data['serial_number']
            model_number = product_form.cleaned_data['model_number']
            description = product_form.cleaned_data['description']
            
            # Check if a product with the same serial number exists
            existing_product = Product.objects.filter(serial_number=serial_number).first()
            serial_number_with_company = f"{serial_number} -- {existing_company.company_name}"
            
            if existing_product:
                # Find a unique serial number by appending a counter
                counter = 0
                new_serial_number = serial_number_with_company
                while Product.objects.filter(serial_number=new_serial_number).exists():
                    print("Entering loop to find unique serial number")
                    counter += 1
                    new_serial_number = f"{serial_number_with_company} -- {counter}"
            
                # Create a new product record with the unique serial number
                new_product = product_form.save(commit=False)
                new_product.serial_number = new_serial_number
                new_product.product_name = product_name
                new_product.model_number = model_number
                new_product.description = description
                new_product.save()
            else:
                # Create a new product record with the original serial number and company name
                new_product = product_form.save(commit=False)
                new_product.serial_number = serial_number_with_company
                new_product.product_name = product_name
                new_product.model_number = model_number
                new_product.description = description
                new_product.save()
            
            # Ticket details
            location = ticket.cleaned_data['location_text']
            issue = ticket.cleaned_data['issue']
            downtime_required = ticket.cleaned_data['downtime_required']
            spare_by_zaco = ticket.cleaned_data['spare_by_zaco']
            problem = ticket.cleaned_data['problem']
            address = ticket.cleaned_data['address']
            sales_person = ticket.cleaned_data['sales_person']
            
            ticket1 = ticket.save(commit=False)
            ticket1.raised_by = request.user
            ticket1.phone_number = user_contact_no
            ticket1.company = existing_company
            ticket1.location_text = location
            ticket1.product = new_product
            ticket1.contact_person = request.user
            ticket1.issue = issue
            ticket1.problem = problem
            ticket1.downtime_required = downtime_required
            ticket1.spare_by_zaco = spare_by_zaco
            ticket1.sales_person = sales_person
            ticket1.save()
            
            # Prepare HTML message
            customer_email = request.user.email
            salesperson_id = request.POST.get('sales_person')
            selected_salesperson = User.objects.filter(pk=salesperson_id).first()
            salesperson_email = selected_salesperson.email if selected_salesperson else None
            
            # Prepare email template and content
            email_template_path = "email/ticket_create_mail.html"
            ticket_link = build_subdomain_absolute_uri(request, "Ticket", pk=ticket1.pk)
            email_content = render_to_string(
                email_template_path,
                {'ticket': ticket1, 'ticket_link': ticket_link}
            )
            subject = f"New Ticket Created - Ticket ID: {ticket1.uuid}"
            email_from = 'info@zacocomputer.com'
            
            # For sending email to customer
            email_thread = Thread(target=send_email_async, args=(subject, email_content, email_from, [customer_email]))
            email_thread.start()
            
            # For sending email to salesperson
            if salesperson_email:
                email_thread = Thread(target=send_email_async, args=(subject, email_content, email_from, [salesperson_email]))
                email_thread.start()
            
            return redirect('dashboard')
        else:
            print("Form errors:")
            print("Product Form Errors:", product_form.errors)
            print("Ticket Form Errors:", ticket.errors)
    
    else:
        product_form = ProductForm()
    
    context = {
        'product_form': product_form,
        'saleuser': saleuser,
        'ticket': ticket,
    }
    
    return render(request, 'support/non-amc-cus.html', context)


def get_product_details(request):
    if request.method == 'GET':
        serial_number = request.GET.get('serial_number')
        
        if serial_number:
            product = Product.objects.filter(serial_number=serial_number).first()
            
            if product:
                return JsonResponse({
                    'product_name': product.product_name,
                    'model_number': product.model_number,
                    'description': product.description,
                    # Add other attributes as needed
                })
            else:
                return JsonResponse({'error': 'Product not found for serial number'}, status=404)
        else:
            return JsonResponse({'error': 'Serial number parameter is missing'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
