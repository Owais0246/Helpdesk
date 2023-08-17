from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect,reverse
from django.views import generic
from django.contrib import messages
from user.models import User
from .forms import CreateUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.


# Create View

class  UserCreateView(generic.CreateView):
    user=User.objects.all()
    template_name='users/user_create.html'
    form_class=CreateUser
    context = user
    def get_success_url(self):
        messages.success(self.request, 'User Created Successfully')
        return reverse ("UserList")

# List View
class UserListView(generic.ListView):
    template_name = "users/user_list.html"
    queryset = User.objects.all()
    context_object_name = "users"

# Detail View

def UserDetail(request, pk):
    user_pk =User.objects.get(id=pk)

    context = {
        "users": user_pk,
    }
    return render(request, 'users/user_detail.html', context)
    

# User Update View

# class UserUpdateView(generic.UpdateView):
#     template_name="users/user_update.html"
#     form_class = UpdateUser
#     queryset = User.objects.all()
#     context_object_name = "users"
    
    
#     def get_success_url(self):
#         return reverse ("UserList")


# User Login view

def LoginPage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username Or Password Is Incorrect')
            
        context = {}
        return render(request, 'users/login.html', context)


# User Logout View

def LogoutUser (request):
    logout(request)
    return redirect ('Login')


# @method_decorator(login_required, name='dispatch')
# class Dashboard(generic.TemplateView):
#     template_name= "dashboard/dashboard.html"