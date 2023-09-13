from django.urls import path
from support import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ticket', views.create_ticket, name="CreateTicket"),
    path('list', views.ticket_list, name="TicketList"),
    path('ticket/<int:pk>', views.ticket, name="Ticket"),
    
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

