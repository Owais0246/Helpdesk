from django.contrib import admin
from .models import Ticket, Document, Call_Time, CallDocument, Message, MessageDocument, SpareCost

class TicketAdmin(admin.ModelAdmin):
    list_display = ('issue', 'uuid', 'raised_by', 'company', 'location', 'product', 'status', 'priority', 'created_at', 'closed_at')
    list_filter = ('status', 'priority', 'created_at', 'closed_at')
    search_fields = ('issue', 'uuid', 'raised_by__username', 'company__company_name', 'location__loc_name', 'product__product_name')
    date_hierarchy = 'created_at'
    readonly_fields = ('uuid',)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file',)

class Call_TimeAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'schedule', 'clock_in', 'clock_out', 'update', 'field_engineer')
    list_filter = ('schedule', 'field_engineer')
    date_hierarchy = 'schedule'

class CallDocumentAdmin(admin.ModelAdmin):
    list_display = ('call_time', 'file')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sent_on', 'messages', 'sender')

class MessageDocumentAdmin(admin.ModelAdmin):
    list_display = ('message', 'file')

class SpareCostAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'type', 'part_no', 'sr_no', 'cost')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Call_Time, Call_TimeAdmin)
admin.site.register(CallDocument, CallDocumentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageDocument, MessageDocumentAdmin)
admin.site.register(SpareCost, SpareCostAdmin)
