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
    path('<int:pk>', views.UserDetail, name="UserDetail")
]
