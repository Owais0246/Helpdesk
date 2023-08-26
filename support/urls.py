from django.urls import path
from support import views

urlpatterns = [
    path('ticket', views.create_ticket, name="CreateTicket"),
    
    ]
