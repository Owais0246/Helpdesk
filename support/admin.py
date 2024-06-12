
"""
Admin module for managing ticket-related models.

This module contains admin classes for Ticket, Document, Call_Time, CallDocument,
Message, MessageDocument, and SpareCost models.

Classes:
    TicketAdmin: Admin class for Ticket model.
    DocumentAdmin: Admin class for Document model.
    Call_TimeAdmin: Admin class for Call_Time model.
    CallDocumentAdmin: Admin class for CallDocument model.
    MessageAdmin: Admin class for Message model.
    MessageDocumentAdmin: Admin class for MessageDocument model.
    SpareCostAdmin: Admin class for SpareCost model.

Registers the admin classes for the respective models.
"""
from django.contrib import admin
from .models import Ticket, Document, Call_Time, CallDocument, Message, MessageDocument, SpareCost

class TicketAdmin(admin.ModelAdmin):
    """
    Admin class for Ticket model.

    This class customizes the display and behavior of 
    the Ticket model in the Django admin interface.
    """

    list_display = (
        'issue', 'uuid', 'raised_by', 'company', 'location', 'product',
        'status', 'priority', 'created_at', 'closed_at'
    )
    list_filter = ('status', 'priority', 'created_at', 'closed_at')
    search_fields = (
        'issue', 'uuid', 'raised_by__username', 'company__company_name',
        'location__loc_name', 'product__product_name'
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('uuid',)


class DocumentAdmin(admin.ModelAdmin):
    """
    Admin class for Document model.

    This class customizes the display of Document objects in the Django admin interface.
    """

    list_display = ('file',)


class CallTimeAdmin(admin.ModelAdmin):
    """
    Admin class for Call_Time model.

    This class customizes the display and filtering of 
    Call_Time objects in the Django admin interface.
    """

    list_display = ('ticket_id', 'schedule', 'clock_in', 'clock_out', 'update', 'field_engineer')
    list_filter = ('schedule', 'field_engineer')
    date_hierarchy = 'schedule'


class CallDocumentAdmin(admin.ModelAdmin):
    """
    Admin class for CallDocument model.

    This class customizes the display of CallDocument objects in the Django admin interface.
    """

    list_display = ('call_time', 'file')


class MessageAdmin(admin.ModelAdmin):
    """
    Admin class for Message model.

    This class customizes the display of Message objects in the Django admin interface.
    """

    list_display = ('sent_on', 'messages', 'sender')


class MessageDocumentAdmin(admin.ModelAdmin):
    """
    Admin class for MessageDocument model.

    This class customizes the display of MessageDocument objects in the Django admin interface.
    """

    list_display = ('message', 'file')

class SpareCostAdmin(admin.ModelAdmin):
    """
    Admin class for SpareCost model.

    This class customizes the display of SpareCost objects in the Django admin interface.
    """

    list_display = ('ticket', 'type', 'part_no', 'sr_no', 'cost')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Call_Time, CallTimeAdmin)
admin.site.register(CallDocument, CallDocumentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageDocument, MessageDocumentAdmin)
admin.site.register(SpareCost, SpareCostAdmin)
