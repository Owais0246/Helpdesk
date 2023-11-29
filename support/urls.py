from django.urls import path
from support import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ticket', views.create_ticket, name="CreateTicket"),
    path('list', views.ticket_list, name="TicketList"),
    path('ticket/<int:pk>', views.ticket, name="Ticket"),
    path('clock_in/<int:pk>', views.clock_in, name="ClockIn"),
    path('clock_out/<int:pk>', views.clock_out, name="ClockOut"),
    # path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('download/<int:file_id>/<str:file_type>/', views.download_file, name='download_file'),
    path('view_attachment/<int:attachment_id>/', views.view_attachment, name='view_attachment'),


    

    
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

