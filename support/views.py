from threading import Thread
import os
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.core.mail import send_mail

# from django.db.models import Q
from django.contrib.auth.decorators import login_required

# from amc.models import Amc
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from user.models import User
from masters.models import Product, Location
from .models import Ticket, Document, Call_Time, MessageDocument, CallDocument
from .forms import TicketForm, AssignTicketForm, CloseForm, ClockIn, ClockOutForm
from .utils import build_absolute_url


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
    if user.is_customer_admin:
        product = Product.objects.filter(amc__company_id=user.user_company.pk)

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
            ticket.save()
            for doc in request.FILES.getlist("documents"):
                ticket.documents.create(
                    file=doc
                )  # Create Document objects and associate them with the ticket

            email_template_path = "email/ticket_create_mail.html"
            email_content = render_to_string(
                email_template_path,
                {
                    "ticket": ticket,
                    "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
                },
            )
            subject = f" New Ticket Created - Ticket ID: {ticket.uuid}"
            message = email_content
            email_from = "info@zacocomputer.com"
            recipient_list = [ticket.raised_by.email] + admin_email

            email_thread = Thread(
                target=send_email_async,
                args=(subject, message, email_from, recipient_list),
            )
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
    ticket = Ticket.objects.all()
    ticket_user = Ticket.objects.filter(assignee=request.user)
    ticket_active = Ticket.objects.filter(assignee=request.user).filter(status="Open")
    ticket_close = Ticket.objects.filter(assignee=request.user).filter(status="Closed")

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
    customer_admin = User.objects.filter(user_loc=ticket.location).filter(
        is_customer_admin=True
    )
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
    call_filter = Call_Time.objects.filter(ticket_id=pk).filter(
        field_engineer=request.user
    )

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
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
            },
        )

        subject = f"""Ticket Assignment Confirmation - Ticket ID: {ticket.uuid}"""
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [ticket.assignee.email, ticket.raised_by.email]
        print(recipient_list)
        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
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
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
                "field_engineer": field_engineer,
                "schedule": schedule,
            },
        )

        subject = f"Service Schedule and Engineer Assigned  - Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [field_engineer.email, ticket.raised_by.email]
        print(recipient_list)

        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
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
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
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
        print(assign_email)
        return redirect("Ticket", pk)

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
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
            },
        )
        subject = f"Ticket ID {ticket.uuid} New Message"
        message = email_content
        email_from = "info@zacocomputer.com"
        recipient_list = [assign_email, ticket.raised_by.email]
        if customer_admin:
            for admin in customer_admin:
                if admin.email not in recipient_list:
                    recipient_list.append(admin.email)
        if sender.email in recipient_list:
            recipient_list.remove(sender.email)
        print(recipient_list)
        # print(customer_admin.values())

        # Use threading to send the email asynchronously
        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
        email_thread.start()

        return redirect("Ticket", pk)

    elif "close" in request.POST:
        feedback = request.POST.get("feedback")
        status = "Closed"
        closed_at = datetime.datetime.now()
        time = closed_at.strftime("%d/%m/%Y, %I:%M:%S %p")
        ticket1.update(feedback=feedback, status=status, closed_at=closed_at)
        ticket.ticket_message.create(
            messages=f"""Your ticket {ticket.uuid} has been successfully closed at {time}. Here is a summary of the ticket:
                                                {feedback}
                                                If you have any further questions or need assistance, feel free to reach out.""",
            sender=request.user,
        )

        email_template_path = "email/ticket_close_email.html"
        email_content = render_to_string(
            email_template_path,
            {
                "ticket": ticket,
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
                "time": time,
                "feedback": feedback,
            },
        )

        subject = f"Ticket Closure Notification - Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [assign_email, ticket.raised_by.email]
        if customer_admin:
            for admin in customer_admin:
                if admin.email not in recipient_list:
                    recipient_list.append(admin.email)
        if sender.email in recipient_list:
            recipient_list.remove(sender.email)
        print(recipient_list)

        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
        email_thread.start()

        return redirect("Ticket", pk)

    elif "transport_cost" in request.POST:
        fe_cost = request.POST.get("fe_cost")
        spare_cost = request.POST.get("spare_cost")
        transport_cost = request.POST.get("transport_cost")
        amount_return = request.POST.get("amount_return")
        Ticket.objects.filter(pk=pk).update(
            fe_cost=fe_cost,
            spare_cost=spare_cost,
            transport_cost=transport_cost,
            amount_return=amount_return,
        )
        return redirect("Ticket", pk)

    costing = 0
    exp = 0
    if (
        ticket.transport_cost is not None
        and ticket.spare_cost is not None
        and ticket.fe_cost
    ):
        costing = ticket.transport_cost + ticket.spare_cost + ticket.fe_cost
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
    return render(request, "support/ticket.html", context)


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
    customer_admin = User.objects.filter(user_loc=ticket.location).filter(
        is_customer_admin=True
    )
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
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
                "time": time,
                "call": call,
            },
        )

        subject = f"Field Engineer Arrival Notification - Service for Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [assign_email, ticket.raised_by.email]
        if customer_admin:
            for admin in customer_admin:
                if admin.email not in recipient_list:
                    recipient_list.append(admin.email)

        print(recipient_list)

        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
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
    customer_admin = User.objects.filter(user_loc=ticket.location).filter(
        is_customer_admin=True
    )
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
                "ticket_link": build_absolute_url(request, "Ticket", pk=ticket.pk),
                "time": time,
                "call": call,
                "update": update,
            },
        )

        subject = f"Field Engineer Departure Notification - Service Summary for Ticket ID: {ticket.uuid}"
        message = email_content
        email_from = "info@zacocomputer.com"  # Your Gmail address from which you want to send emails
        recipient_list = [assign_email, ticket.raised_by.email]
        if customer_admin:
            for admin in customer_admin:
                if admin.email not in recipient_list:
                    recipient_list.append(admin.email)

        print(recipient_list)

        email_thread = Thread(
            target=send_email_async, args=(subject, message, email_from, recipient_list)
        )
        email_thread.start()

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
