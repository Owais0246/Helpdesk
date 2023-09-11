from django.urls import path
from support import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ticket', views.create_ticket, name="CreateTicket"),
    path('list', views.ticket_list, name="TicketList"),
    
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

