from django.urls import path
from support import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_spare_cost_form

urlpatterns = [
    path('ticket', views.create_ticket, name="CreateTicket"),
    path('list', views.ticket_list, name="TicketList"),
    path('ticket/<int:pk>', views.ticket, name="Ticket"),
    path('clock_in/<int:pk>', views.clock_in, name="ClockIn"),
    path('clock_out/<int:pk>', views.clock_out, name="ClockOut"),
    # path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('download/<int:file_id>/<str:file_type>/', views.download_file, name='download_file'),
    path('view_attachment/<int:attachment_id>/', views.view_attachment, name='view_attachment'),
    path('spare_cost_form/', get_spare_cost_form, name='get_spare_cost_form'),

    path('generate_ticket/', views.generate_ticket, name='generate_ticket'),
    path('generate_ticket_cus/', views.generate_ticket_cus, name='generate_ticket_cus'),

    

    
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

