'''Masters Views'''
from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from user.forms import CreateUser
from user.models import User
from amc.forms import CreateAmcForm
from amc.models import Amc
from .forms import CompanyForm,LocationForm,ProductForm
from . models import Company,Location,Product
from django.db.models import Max
from django.utils.text import slugify

# Create your views here.

def get_company_details(request):
    '''Get Company data for Ajax'''
    company_name = request.GET.get('company_name', None)
    if company_name:
        try:
            company = Company.objects.filter(company_name=company_name).first()
            data = {
                'company_contact_no': company.company_contact_no,
                'address': company.address,
            }
            return JsonResponse(data)
        except Company.DoesNotExist:
            pass
    
    return JsonResponse({'error': 'Company not found'})


def get_product_details(request):
    '''Get Product data for Ajax'''
    serial_number = request.GET.get('serial_number', None)
    if serial_number:
        try:
            products = Product.objects.filter(serial_number=serial_number).first()
            data = {
                'product_name': products.product_name,
                'model_number': products.model_number,
                'description': products.description,
            }
            return JsonResponse(data)
        except Product.DoesNotExist:  # Corrected exception handling
            pass
    
    return JsonResponse({'error': 'Product not found'})


def get_user_details(request):
    '''Get User data for Ajax'''
    email = request.GET.get('email', None)
    if email:
        try:
            user = User.objects.filter(email=email).first()
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_contact_no': user.user_contact_no,
            }
            return JsonResponse(data)
        except User.DoesNotExist:  # Corrected exception handling
            pass
    
    return JsonResponse({'error': 'User not found'})


#Company Views

@login_required
def create_customer(request):
    customer_form = CompanyForm(request.POST)
    if customer_form.is_valid():
        form = customer_form.save(commit=False)
        company_suffix = form.company_suffix
        if company_suffix:
            # Check if the company_suffix already exists
            existing_suffixes = Company.objects.filter(company_suffix=company_suffix)
            if existing_suffixes.exists():
                # Get the highest suffix number
                max_suffix_number = existing_suffixes.aggregate(Max('company_suffix'))['company_suffix__max']
                if max_suffix_number is not None:
                    # Increment the suffix number
                    suffix_parts = company_suffix.split('-')
                    if len(suffix_parts) == 1:
                        # If no number present, append -1
                        new_suffix = f"{company_suffix}-1"
                    else:
                        # If number present, increment it
                        suffix_number = int(suffix_parts[-1])
                        new_suffix = "-".join(suffix_parts[:-1]) + f"-{suffix_number + 1}"
                    # Check if the newly generated suffix exists
                    while Company.objects.filter(company_suffix=new_suffix).exists():
                        # Increment the suffix number until a unique value is found
                        suffix_parts = new_suffix.split('-')
                        suffix_number = int(suffix_parts[-1])
                        new_suffix = "-".join(suffix_parts[:-1]) + f"-{suffix_number + 1}"
                    form.company_suffix = new_suffix
        form.is_customer = True
        form.save()
        return redirect('CompanyList')

    context = {
        'customer_form': customer_form,
        # 'company': company,
    }
    return render(request, 'masters/company/company_create.html', context)

@login_required
def customer_list(request):
    customers= Company.objects.filter(is_customer=True)
    context= {'customers':customers}
    return render(request, 'masters/company/company_list.html', context)
    
@method_decorator(login_required, name="dispatch")
class CustomerCreateView(generic.CreateView):
    template_name = 'masters/company/company_create.html'
    form_class = CompanyForm

    def get_success_url(self):
        return reverse('CompanyList')
    
    
@method_decorator(login_required, name="dispatch")
class CustomerListView(generic.ListView):
    template_name = 'masters/company/company_list.html'
    queryset = Company.objects.all()
    context_object_name = 'company'
    
    
@login_required
def customer_detail(request, company_pk):
    customer_pk =Company.objects.get(id=company_pk)
    amc =Amc.objects.filter(company=customer_pk)
    
    location_form=LocationForm(request.POST)
    locations=Location.objects.filter(loc_company=customer_pk)
    
    if location_form.is_valid():
        form=location_form.save(commit=False)
        form.loc_company = customer_pk
        form.save()
        location_form.save()
        return redirect('CompanyDetail',company_pk)
    
    context = {
        "customer": customer_pk,
        "location_form":location_form,
        "locations":locations,
        'amc':amc,
            
    }
    return render(request, 'masters/company/company_detail.html', context)

@login_required
def create_customer_user(request,pk):
    print ("create user is working")
    company=Company.objects.get(id=company_pk)
    location=Location.objects.get(id=location_pk)
    user_form =CreateUser(request.POST)
    users =User.objects.filter(user_company=customer_pk)
    
    if user_form.is_valid():
        form= user_form.save(commit=False)
        form.is_customer_user = True
        form.user_company=company
        form.user_loc=location
        form.save()
        return redirect('CompanyDetail', company_pk)
    
    context = {        
        "user_form":user_form,
        "users":users,
        "company":company,
        "location":location
        }
    return render(request, 'masters/company/company_detail.html', context)

    
@method_decorator(login_required, name="dispatch")
class CustomerUpdateView(generic.UpdateView):
    model =Company
    form_class = CompanyForm
    template_name = 'masters/company/company_update.html'

    def get_success_url(self):
        return reverse('CompanyList')


#Location Views
@method_decorator(login_required, name="dispatch")
class LocationCreateView(generic.CreateView):
    template_name = 'masters/location/location_create.html'
    form_class = LocationForm

    def get_success_url(self):
        return reverse('LocationList')
    

@method_decorator(login_required, name="dispatch")
class LocationListView(generic.ListView):
    template_name = 'masters/location/location_list.html'
    queryset = Location.objects.all()
    context_object_name = 'location'


@login_required
def LocationDetail(request, pk):
    location =Location.objects.get(id=pk)
    company =Company.objects.get(id=location.loc_company.pk)
    # amc = Amc.objects.filter(company=company)

    
    user_form =CreateUser(request.POST)
    users =User.objects.filter(user_loc=location)
    
    amc_form =CreateAmcForm(request.POST)
    amc =Amc.objects.filter(company=company)
    
    products=Product.objects.all()
    
    if user_form.is_valid():
        form= user_form.save(commit=False)
        form.is_customer_user = True
        form.user_company=company
        form.user_loc=location
        form.save()
        messages.success(request, 'User Created Successfully')
        return redirect('LocationDetail',pk)
    
    if amc_form.is_valid():
        form= amc_form.save(commit=False)
        form.company=company
        form.location=location
        # form.user=users
        form.save()
        messages.success(request, 'User Created Successfully')
        return redirect('LocationDetail',pk)
    
    context = {        
        "user_form":user_form,
        "users":users,
        "customer":company, 
        "location":location,
        "products":products,
        "amc":amc,
        }
   
    return render(request, 'masters/location/location_detail.html', context)

@method_decorator(login_required, name="dispatch")
class LocationUpdateView(generic.UpdateView):
    model =Location
    form_class = LocationForm
    template_name = 'masters/location/location_update.html'

    def get_success_url(self):
        return reverse('LocationList')
    
    
#Product Views
@method_decorator(login_required, name="dispatch")
class ProductCreateView(generic.CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('ProductList')
    
@method_decorator(login_required, name="dispatch")
class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

@login_required
def ProductDetail(request, pk):
    product_pk =Product.objects.get(id=pk)

    context = {
        "product": product_pk,
    }
    return render(request, 'product/product_detail.html', context)

@method_decorator(login_required, name="dispatch")
class ProductUpdateView(generic.UpdateView):
    model =Product
    form_class =ProductForm
    template_name = 'product/product_update.html'

    def get_success_url(self):
        return reverse('ProductList')
    
@login_required
def LoadLocation(request):
    company=request.GET.get('company')
    location= Location.objects.filter(loc_company=company) 
    location_data = serialize('json', location)
    # Returning the JSON response
    return JsonResponse({'location_list': location_data}, safe=False)
    # return JsonResponse(location_data, safe=False)