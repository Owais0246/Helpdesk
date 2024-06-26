# from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect,reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.models import User
from masters.models import Company
from .forms import *


from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm

# Create your views here.


# **************users list view*****************
@login_required
def user_list_view(request):
    service_admin_view = User.objects.filter(is_service_admin=True)
    service_agent_view = User.objects.filter(is_service_agent=True)
    # customer_user_view = User.objects.filter(is_customer_user=True)
    # customer_admin_view = User.objects.filter(is_customer_admin=True)
    field_engineer_view = User.objects.filter(is_field_engineer=True)
    sr_engineer_view = User.objects.filter(is_sr_engineer=True)

    return render(request,'masters/company/users-list.html',{'service_admin_view':service_admin_view,
                                                               'service_agent_view':service_agent_view,
                                                            #    'customer_user_view':customer_user_view,
                                                            #    'customer_admin_view':customer_admin_view,
                                                               'field_engineer_view':field_engineer_view,
                                                               'sr_engineer_view':sr_engineer_view,})


# *****************create service admin view*********************
@login_required
def create_service_admin(request):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    if request.method=="POST":
        service_form = ServiceAdminForm(request.POST, request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_service_admin=True
            service.is_service_agent=True
            service.save()

            return redirect('service-admin-list')
    else:
        service_form = ServiceAdminForm()

    return render(request,'masters/company/service_admin.html',{'service_form':service_form})



# ***************edit service admin view*******************


@login_required
def edit_service_admin(request,pk):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    service_admin = get_object_or_404(User,id=pk)
    if request.method=="POST":
        service_form = ServiceUpdateForm(request.POST, request.FILES, instance=service_admin)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_service_admin=True
            service.is_service_agent=True
            service.save()

            return redirect('service-admin-list')
        else:
            # If the form is not valid, re-render the form with validation errors
            return render(request, 'masters/company/service_admin_edit.html', {'service_form': service_form})
    else:
        service_form = ServiceUpdateForm(instance=service_admin)

    return render(request,'masters/company/service_admin_edit.html',{'service_form':service_form})

def service_admin_del(request,pk):
    service_admin= User.objects.get(id=pk)
    service_admin.delete()
    return redirect('service-admin-list')



# ***************service admin list view*************
@login_required
def service_admin_list(request):
    service_admin_view = User.objects.filter(is_service_admin=True)
    return render(request,'users/service_admin_list.html',{'service_admin_view':service_admin_view})


# **********create service agent view**************

@login_required
def create_service_agent(request):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    if request.method=="POST":
        service_form = ServiceAdminForm(request.POST, request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_service_agent=True
            service.save()

            return redirect('service-agent-list')
    else:
        service_form = ServiceAdminForm()

    return render(request,'masters/company/service_admin.html',{'service_form':service_form})


# *****************edit service agent view****************** 

@login_required
def edit_service_agent(request,pk):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    service_agent = get_object_or_404(User,id=pk)
    if request.method=="POST":
        service_form = ServiceUpdateForm(request.POST, request.FILES, instance=service_agent)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_service_agent=True
            service.save()

            return redirect('service-agent-list')
    else:
        service_form = ServiceUpdateForm(instance=service_agent)

    return render(request,'masters/company/service_admin_edit.html',{'service_form':service_form})


# *****************Delete service agent view****************** 
@login_required
def service_agent_del(request,pk):
    service_agent= User.objects.get(id=pk)
    service_agent.delete()
    return redirect('service-agent-list')


# ***************service agent list view************* 
@login_required
def service_agent_list(request):
    service_agent_view = User.objects.filter(is_service_agent=True)
    return render(request,'users/service_agent_list.html',{'service_agent_view':service_agent_view})





# **********create salesperson view**************

@login_required
def create_salesperson(request):
    company = Company.objects.get(is_self_company=True)
    if request.method == "POST":
        service_form = salesForm(request.POST, request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company = company
            service.is_salesperson = True
            service.user_loc = service_form.cleaned_data['user_loc']  # Assign selected location
            service.save()
            return redirect('salesperson-list')
    else:
        service_form = salesForm()

    return render(request,'masters/company/salesperson.html',{'service_form':service_form})


# *****************edit service agent view****************** 

@login_required
def edit_salesperson(request,pk):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    service_agent = get_object_or_404(User,id=pk)
    if request.method=="POST":
        service_form = salesUpdateForm(request.POST, request.FILES, instance=service_agent)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_salesperson=True
            service.save()

            return redirect('salesperson-list')
    else:
        service_form = salesUpdateForm(instance=service_agent)

    return render(request,'masters/company/salesperson_edit.html',{'service_form':service_form})


# *****************Delete service agent view****************** 
@login_required
def salesperson_del(request,pk):
    salesperson= User.objects.get(id=pk)
    salesperson.delete()
    return redirect('salesperson-list')


# ***************service agent list view************* 
@login_required
def salesperson_list(request):
    salesperson_view = User.objects.filter(is_salesperson=True)
    return render(request,'users/salesperson_list.html',{'salesperson':salesperson_view})



# **********create field engineer********** 
@login_required
def create_field_engineer(request):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    if request.method=="POST":
        service_form = ServiceAdminForm(request.POST, request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_field_engineer=True
            service.save()

            return redirect('field-engineer-list')
    else:
        service_form = ServiceAdminForm()

    return render(request,'masters/company/service_admin.html',{'service_form':service_form})

# **********edit field engineer************* 
@login_required
def edit_field_engineer(request,pk):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    field_engineer = get_object_or_404(User,id=pk)
    if request.method=="POST":
        service_form = ServiceUpdateForm(request.POST, request.FILES, instance=field_engineer)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_field_engineer=True
            service.save()

            return redirect('field-engineer-list')
    else:
        service_form = ServiceUpdateForm(instance=field_engineer)

    return render(request,'masters/company/service_admin_edit.html',{'service_form':service_form})


# **************delete field engineer***************
@login_required
def field_engineer_del(request,pk):
    field_engineer= User.objects.get(id=pk)
    field_engineer.delete()
    return redirect('field-engineer-list')


# ***************Field engineer list view************* 
@login_required
def field_engineer_list(request):
    field_engineer_view = User.objects.filter(is_field_engineer=True)
    return render(request,'users/field_engineer_list.html',{'field_engineer_view':field_engineer_view})


# ***********create sr engineer*************
@login_required
def create_sr_engineer(request):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    if request.method=="POST":
        service_form = ServiceAdminForm(request.POST, request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user_company=company
            service.is_sr_engineer=True
            service.is_field_engineer=True
            service.save()
            return redirect('sr-engineer-list')
    else:
        service_form = ServiceAdminForm()

    return render(request,'masters/company/service_admin.html',{'service_form':service_form})


# **************edit sr engineer*****************
@login_required
def edit_sr_engineer(request,pk):
    # company = get_object_or_404(Company, id=pk)
    company=Company.objects.get(is_self_company=True)
    sr_engineer = get_object_or_404(User,id=pk)
    if request.method=="POST":
        service_form = ServiceUpdateForm(request.POST, request.FILES, instance=sr_engineer)
        if service_form.is_valid():
          
            service_form.save()

            return redirect('users-list')
    else:
        service_form = ServiceUpdateForm(instance=sr_engineer)

    return render(request,'masters/company/service_admin_edit.html',{'service_form':service_form})

# **************delete sr engineer****************
@login_required
def sr_engineer_del(request,pk):
    sr_engineer= User.objects.get(id=pk)
    sr_engineer.delete()
    return redirect('sr-engineer-list')


# ***************senior engineer list view************* 
@login_required
def sr_engineer_list(request):
    sr_engineer_view = User.objects.filter(is_sr_engineer=True)
    return render(request,'users/senior_engineer_list.html',{'sr_engineer_view':sr_engineer_view})

# def create_customer(request):
#     customer_form=CompanyForm(request.POST)
#     if customer_form.is_valid():
#         form= customer_form.save(commit=False)
#         form.is_customer=True
#         form.save()
        
#         return redirect('CompanyList')

#     context = {
#         'customer_form': customer_form,
        
#     }
#     return render(request, 'masters/company/company_create.html', context)

# Create View

@method_decorator(login_required, name="dispatch")
class  UserCreateView(generic.CreateView):
    user=User.objects.all()
    template_name='users/user_create.html'
    form_class=CreateUser
    context = user
    def get_success_url(self):
        messages.success(self.request, 'User Created Successfully')
        return reverse ("UserList")

# List View
@method_decorator(login_required, name="dispatch")
class UserListView(generic.ListView):
    template_name = "users/user_list.html"
    queryset = User.objects.all()
    context_object_name = "users"

# Detail View
@login_required
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

def login_user(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username Or Password Is Incorrect')
            
        context = {}
        return render(request, 'users/login.html', context)


# User Logout View
@login_required
def logout_user (request):
    logout(request)
    return redirect ('login')


# @method_decorator(login_required, name='dispatch')
# class Dashboard(generic.TemplateView):
#     template_name= "dashboard/dashboard.html"




class PasswordResetConfirmView(FormView):
    template_name = 'users/password_reset_confirm.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)