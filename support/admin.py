from django.contrib import admin
from .models import Ticket, Document, Call_Time, Message, CallDocument
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Document)
admin.site.register(Call_Time)
admin.site.register(Message)
admin.site.register(CallDocument)