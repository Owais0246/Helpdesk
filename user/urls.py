from django.urls import path
from user import views
from .views import (
    UserListView,    
    UserCreateView,
   
)


urlpatterns = [
    path('list', UserListView.as_view(), name="UserList"),
    path('add', UserCreateView.as_view(), name="CreateUser"),
    # path('<int:pk>/update', UserUpdateView.as_view(), name="UserUpdate"),
    path('<int:pk>', views.UserDetail, name="UserDetail"),
    path('users-list', views.user_list_view, name="users-list"),

    path('create-service-admin', views.create_service_admin, name="create-service-admin"),
    # path('users-list', views.service_admin_list, name="list-services"),
    path('edit-service-admin/<int:pk>', views.edit_service_admin, name="edit-service-admin"),
    path('delete-service-admin/<int:pk>', views.service_admin_del, name="delete-service-admin"),
    path('service-admin-list', views.service_admin_list, name="service-admin-list"),
    path('create-service-agent', views.create_service_agent, name="create-service-agent"),
    path('delete-service-agent/<int:pk>', views.service_agent_del, name="delete-service-agent"),
    path('edit-service-agent/<int:pk>', views.edit_service_agent, name="edit-service-agent"),
    path('service-agent-list', views.service_agent_list, name="service-agent-list"),
    # path('users-list', views.service_agent_list, name="list-services"),
    # path('create-customer-user', views.create_customer_user, name="create-customer-user"),
    # path('edit-customer-user/<int:pk>', views.edit_customer_user, name="edit-customer-user"),
    # path('create-customer-admin', views.create_customer_admin, name="create-customer-admin"),
    # path('edit-customer-admin/<int:pk>', views.edit_customer_admin, name="edit-customer-admin"),
    path('create-field-engineer', views.create_field_engineer, name="create-field-engineer"),
    path('edit-field-engineer/<int:pk>', views.edit_field_engineer, name="edit-field-engineer"),
    path('delete-field-engineer/<int:pk>', views.field_engineer_del, name="delete-field-engineer"),
    path('field-engineer-list', views.field_engineer_list, name="field-engineer-list"),
    path('create-sr-engineer', views.create_sr_engineer, name="create-sr-engineer"),
    path('edit-sr-engineer/<int:pk>', views.edit_sr_engineer, name="edit-sr-engineer"),
    path('delete-sr-engineer/<int:pk>', views.sr_engineer_del, name="delete-sr-engineer"),
    path('sr-engineer-list', views.sr_engineer_list, name="sr-engineer-list"),
    
    path('create-salesperson', views.create_salesperson, name="create-salesperson"),
    path('edit-salesperson/<int:pk>', views.edit_salesperson, name="edit-salesperson"),
    path('delete-salesperson/<int:pk>', views.salesperson_del, name="delete-salesperson"),
    path('salesperson-list', views.salesperson_list, name="salesperson-list"),

 
    
   
]
