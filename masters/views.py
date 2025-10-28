"""
Masters Views

This module contains views for managing company, location, and product data.

Attributes:
    All views related to managing company, location, and product data.
"""
from django.shortcuts import render,redirect,reverse, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.db.models import Max
from user.forms import CreateUser
from user.models import User
from amc.forms import CreateAmcForm
from amc.models import Amc
from .forms import CompanyForm,LocationForm,ProductForm
from . models import Company,Location,Product


def get_company_details(request):
    """
    Get Company data for Ajax.

    Args:
        request: HttpRequest object containing the HTTP request information.

    Returns:
        JsonResponse: JSON response containing the company data or 
        an error message if the company is not found.
    """
    company_name = request.GET.get('company_name', None)
    if company_name:
        try:
            company = Company.objects.filter(company_name=company_name).first() # pylint: disable=no-member
            data = {
                'company_contact_no': company.company_contact_no,
                'address': company.address,
            }
            return JsonResponse(data)
        except Company.DoesNotExist: # pylint: disable=no-member
            pass

    return JsonResponse({'error': 'Company not found'})


def get_product_details(request):
    """
    Get Product data for Ajax.

    Args:
        request: HttpRequest object containing the HTTP request information.

    Returns:
        JsonResponse: JSON response containing the product data or 
        an error message if the product is not found.
    """
    serial_number = request.GET.get('serial_number', None)
    if serial_number:
        try:
            products = Product.objects.filter(serial_number=serial_number).first() # pylint: disable=no-member
            data = {
                'product_name': products.product_name,
                'model_number': products.model_number,
                'description': products.description,
            }
            return JsonResponse(data)
        except Product.DoesNotExist:  # Corrected exception handling # pylint: disable=no-member
            pass

    return JsonResponse({'error': 'Product not found'})


def get_user_details(request):
    """
    Get User data for Ajax.

    Args:
        request: HttpRequest object containing the HTTP request information.

    Returns:
        JsonResponse: JSON response containing the user data or
        an error message if the user is not found.
    """
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
        except User.DoesNotExist:  # Corrected exception handling # pylint: disable=no-member
            pass

    return JsonResponse({'error': 'User not found'})


#Company Views

@login_required
def create_customer(request):
    """
    Create a new customer.

    This view handles the creation of a new customer. It validates the company form, 
    generates a unique company suffix if necessary,
    and saves the new company to the database.

    Args:
        request: HttpRequest object containing the HTTP request information.

    Returns:
        HttpResponse: Redirects to the CompanyList page if the form is valid 
        and the company is successfully created. 
        Otherwise, renders the company creation form page with the validation errors.
    """

    customer_form = CompanyForm(request.POST)
    if customer_form.is_valid():
        form = customer_form.save(commit=False)
        company_suffix = form.company_suffix
        if company_suffix:
            # Check if the company_suffix already exists
            existing_suffixes = Company.objects.filter(company_suffix=company_suffix) # pylint: disable=no-member
            if existing_suffixes.exists():
                # Get the highest suffix number
                max_suffix_number = existing_suffixes.aggregate(
                    Max('company_suffix'))['company_suffix__max']
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
                    while Company.objects.filter(company_suffix=new_suffix).exists(): # pylint: disable=no-member

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
        # 'company': form,
    }
    return render(request, 'masters/company/company_create.html', context)



def edit_customer(request, pk):
    """
    Edit an existing customer.

    This view allows editing an existing customer's information.
    It reuses the same form and template as customer creation.

    Args:
        request: HttpRequest object containing request data.
        pk: Primary key (ID) of the customer to edit.

    Returns:
        HttpResponse: Redirects to CompanyList if the form is valid.
        Otherwise, renders the form again with validation errors.
    """
    customer = get_object_or_404(Company, pk=pk, is_customer=True)

    if request.method == 'POST':
        customer_form = CompanyForm(request.POST, instance=customer)
        if customer_form.is_valid():
            form = customer_form.save(commit=False)

            # Handle suffix update only if changed
            company_suffix = form.company_suffix
            if company_suffix:
                existing_suffixes = Company.objects.filter(
                    company_suffix=company_suffix
                ).exclude(pk=customer.pk)  # Exclude the current record

                if existing_suffixes.exists():
                    max_suffix_number = existing_suffixes.aggregate(
                        Max('company_suffix')
                    )['company_suffix__max']

                    if max_suffix_number is not None:
                        suffix_parts = company_suffix.split('-')
                        if len(suffix_parts) == 1:
                            new_suffix = f"{company_suffix}-1"
                        else:
                            suffix_number = int(suffix_parts[-1])
                            new_suffix = "-".join(suffix_parts[:-1]) + f"-{suffix_number + 1}"

                        # Ensure uniqueness
                        while Company.objects.filter(company_suffix=new_suffix).exists():
                            suffix_parts = new_suffix.split('-')
                            suffix_number = int(suffix_parts[-1])
                            new_suffix = "-".join(suffix_parts[:-1]) + f"-{suffix_number + 1}"

                        form.company_suffix = new_suffix

            form.is_customer = True
            form.save()
            return redirect('CompanyList')
    else:
        customer_form = CompanyForm(instance=customer)

    context = {
        'customer_form': customer_form,
        'customer': customer,
        'is_edit': True,  # flag to let the template know it's edit mode
    }
    return render(request, 'masters/company/company_create.html', context)



@login_required
def customer_list(request):
    """
    Display the list of customers.

    This view retrieves all customers from the database and 
    renders the customer list page with the customer data.

    Args:
        request: HttpRequest object containing the HTTP request information.

    Returns:
        HttpResponse: Renders the customer list page with the list of customers.
    """

    customers= Company.objects.filter(is_customer=True) # pylint: disable=no-member
    context= {'customers':customers}
    return render(request, 'masters/company/company_list.html', context)


@method_decorator(login_required, name="dispatch")
class CustomerCreateView(generic.CreateView):
    """
    Customer creation view.

    This class-based view handles the creation of new customers. 
    It renders a form for creating a new customer and handles form submission.

    Attributes:
        template_name (str): The name of the template used to render the customer creation form.
        form_class (class): The form class used for creating a new customer.
        
    Methods:
        get_success_url: Returns the URL to redirect to after successfully creating a new customer.

    Returns:
        HttpResponse: Renders the customer creation form or 
        redirects to the success URL after form submission.
    """

    template_name = 'masters/company/company_create.html'
    form_class = CompanyForm

    def get_success_url(self):
        return reverse('CompanyList')


@method_decorator(login_required, name="dispatch")
class CustomerListView(generic.ListView):
    """
    Customer list view.

    This class-based view displays a list of all customers.

    Attributes:
        template_name (str): The name of the template used to render the customer list.
        queryset (QuerySet): The queryset used to fetch all customer objects.
        context_object_name (str): The name of the context variable 
                                    containing the list of customers.

    Returns:
        HttpResponse: Renders the customer list template with the list of customers as context.
    """

    template_name = 'masters/company/company_list.html'
    queryset = Company.objects.all() # pylint: disable=no-member
    context_object_name = 'company'


@login_required
def customer_detail(request, company_pk):
    """
    Customer detail view.

    This function-based view displays the details of a specific customer.

    Args:
        request (HttpRequest): The HTTP request object.
        company_pk (int): The primary key of the company whose details are to be displayed.

    Returns:
        HttpResponse: Renders the customer detail template 
        with the specified customer's details as context.
    """

    customer_pk =Company.objects.get(id=company_pk) # pylint: disable=no-member
    amc =Amc.objects.filter(company=customer_pk) # pylint: disable=no-member

    location_form=LocationForm(request.POST)
    locations=Location.objects.filter(loc_company=customer_pk) # pylint: disable=no-member

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

# @login_required
# def create_customer_user(request,pk):
#     print ("create user is working")
#     company=Company.objects.get(id=company_pk) # pylint: disable=no-member
#     location=Location.objects.get(id=location_pk) # pylint: disable=no-member
#     user_form =CreateUser(request.POST)
#     users =User.objects.filter(user_company=customer_pk) # pylint: disable=no-member

#     if user_form.is_valid():
#         form= user_form.save(commit=False)
#         form.is_customer_user = True
#         form.user_company=company
#         form.user_loc=location
#         form.save()
#         return redirect('CompanyDetail', pk)

#     context = {
#         "user_form":user_form,
#         "users":users,
#         "company":company,
#         "location":location
#         }
#     return render(request, 'masters/company/company_detail.html', context)


@method_decorator(login_required, name="dispatch")
class CustomerUpdateView(generic.UpdateView):
    """
    Customer update view.

    This class-based view handles the updating of customer details.

    Attributes:
        model (Company): The model to be used for updating customer details.
        form_class (CompanyForm): The form class for updating customer details.
        template_name (str): The template to be rendered for updating customer details.
        
        Methods:
        get_success_url: Returns the URL to redirect to after successfully updating a customer.
    """

    model =Company
    form_class = CompanyForm
    template_name = 'masters/company/company_update.html'

    def get_success_url(self):
        return reverse('CompanyList')


#Location Views
@method_decorator(login_required, name="dispatch")
class LocationCreateView(generic.CreateView):
    """
    Location create view.

    This class-based view handles the creation of locations.

    Attributes:
        template_name (str): The template to be rendered for creating locations.
        form_class (LocationForm): The form class for creating locations.

    Methods:
        get_success_url: Returns the URL to redirect to after successfully creating a location.
    """

    template_name = 'masters/location/location_create.html'
    form_class = LocationForm

    def get_success_url(self):
        return reverse('LocationList')


@method_decorator(login_required, name="dispatch")
class LocationListView(generic.ListView):
    """
    Location list view.

    This class-based view handles the listing of locations.

    Attributes:
        template_name (str): The template to be rendered for listing locations.
        queryset (QuerySet): The queryset containing all locations.
        context_object_name (str): The name of the context variable 
                                    containing the list of locations.

    Methods:
        None
    """

    template_name = 'masters/location/location_list.html'
    queryset = Location.objects.all() # pylint: disable=no-member
    context_object_name = 'location'


@login_required
def location_detail(request, pk):
    """
    Location detail view.

    This function-based view handles the display and management of location details.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the location to be displayed.

    Returns:
        HttpResponse: The HTTP response containing the rendered template and context data.

    Attributes:
        None

    Raises:
        None
    """

    location =Location.objects.get(id=pk) # pylint: disable=no-member
    company =Company.objects.get(id=location.loc_company.pk) # pylint: disable=no-member
    # amc = Amc.objects.filter(company=company)


    user_form =CreateUser(request.POST)
    users =User.objects.filter(user_loc=location)

    amc_form =CreateAmcForm(request.POST)
    amc =Amc.objects.filter(company=company) # pylint: disable=no-member

    products=Product.objects.all() # pylint: disable=no-member

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
    """
    Location update view.

    This class-based view allows users to update location details.

    Attributes:
        model (Location): The model class for locations.
        form_class (LocationForm): The form class for updating locations.
        template_name (str): The name of the template used for rendering the update view.

    Methods:
        get_success_url: Returns the URL to redirect to after a successful update operation.

    Raises:
        None
    """

    model =Location
    form_class = LocationForm
    template_name = 'masters/location/location_update.html'

    def get_success_url(self):
        return reverse('LocationList')


#Product Views
@method_decorator(login_required, name="dispatch")
class ProductCreateView(generic.CreateView):
    """
    Product create view.

    This class-based view allows users to create new products.

    Attributes:
        template_name (str): The name of the template used for rendering the create view.
        form_class (ProductForm): The form class for creating products.

    Methods:
        get_success_url: Returns the URL to redirect to after a successful creation operation.

    Raises:
        None
    """

    template_name = 'product/product_create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('ProductList')

@method_decorator(login_required, name="dispatch")
class ProductListView(generic.ListView):
    """
    Product list view.

    This class-based view displays a list of existing products.

    Attributes:
        template_name (str): The name of the template used for rendering the list view.
        queryset (QuerySet): The queryset used to retrieve the list of products.
        context_object_name (str): The name of the context variable containing the list of products.

    Methods:
        None

    Raises:
        None
    """

    template_name = 'product/product_list.html'
    queryset = Product.objects.all() # pylint: disable=no-member
    context_object_name = 'product'

@login_required
def product_detail(request, pk):
    """
    Product detail view.

    This function-based view displays the details of a specific product.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the product to be displayed.

    Returns:
        HttpResponse: The HTTP response containing the rendered product detail template.

    Raises:
        DoesNotExist: If the requested product does not exist.
    """

    product_pk =Product.objects.get(id=pk) # pylint: disable=no-member

    context = {
        "product": product_pk,
    }
    return render(request, 'product/product_detail.html', context)

@method_decorator(login_required, name="dispatch")
class ProductUpdateView(generic.UpdateView):
    """
    Product update view.

    This class-based view handles the updating of product information.

    Attributes:
        model (Model): The model class to be used for updating products.
        form_class (Form): The form class to be used for updating product information.
        template_name (str): The name of the template used for rendering the product update form.

    Methods:
        get_success_url: Returns the URL to redirect to after a successful update.

    Returns:
        HttpResponse: The HTTP response containing the product update form.

    Raises:
        None
    """

    model =Product
    form_class =ProductForm
    template_name = 'product/product_update.html'

    def get_success_url(self):
        return reverse('ProductList')

@login_required
def load_location(request):
    """
    Load location view.

    This function loads locations based on the selected company using AJAX.

    Args:
        request (HttpRequest): The HTTP request object containing GET parameters.

    Returns:
        JsonResponse: The JSON response containing the list of locations.

    Raises:
        None
    """

    company=request.GET.get('company')
    location= Location.objects.filter(loc_company=company) # pylint: disable=no-member
    location_data = serialize('json', location)
    # Returning the JSON response
    return JsonResponse({'location_list': location_data}, safe=False)
    # return JsonResponse(location_data, safe=False)
