"""
Views for the AMC (Annual Maintenance Contract) application.

This module contains views for handling AMC-related operations such as creating, listing, updating,
and detailing AMC instances. It also includes views for loading contact persons dynamically.

Views:
    - create_amc: View for creating a new AMC instance.
    - AmcListView: View for listing all AMC instances.
    - AmcDetail: View for displaying details of a specific AMC instance.
    - AmcUpdateView: View for updating an existing AMC instance.
    - load_contact_person: View for dynamically loading contact persons based on a selected product.
"""
from django.shortcuts import render,redirect,reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.db.models import Sum
from masters.models import Company,Location,Product
from user.models import User
from . models import Amc, Source, Service
from .forms import CreateAmcForm, ProductForm, AMCForm


@login_required
def create_amc(request, pk):
    """
    View for creating a new AMC (Annual Maintenance Contract) instance.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the company.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the specified company does not exist.

    """
    company = Company.objects.get(id=pk) # pylint: disable=no-member
    location = Location.objects.filter(loc_company=company)  # pylint: disable=no-member
    sales_user = User.objects.filter(is_salesperson = True)
    print(sales_user)
    ProductFormSet = inlineformset_factory(Amc, Product, form=ProductForm, extra=1) # pylint: disable=invalid-name
    source = Source.objects.all() # pylint: disable=no-member
    service = Service.objects.all() # pylint: disable=no-member

    if request.method == 'POST':
        amc_form = AMCForm(request.POST, request.FILES)
        product_formset = ProductFormSet(request.POST, request.FILES, instance=Amc(company=company))

        if amc_form.is_valid() and product_formset.is_valid():
            amc_instance = amc_form.save(commit=False)
            amc_instance.company = company
            amc_instance.save()

            product_formset.instance = amc_instance
            product_formset.save()

            # Redirect or render a success page after form submission
            return redirect('CompanyDetail', pk)
        print(amc_form.errors)
    else:
        amc_form = AMCForm()
        product_formset = ProductFormSet(instance=Amc(company=company))
    print(amc_form.errors)
    return render(request, 'amc/amc_create.html', {'amc_form': amc_form,
                                                   'product_formset': product_formset, 
                                                   'locations': location, 
                                                   'company': company,
                                                   'sales_user':sales_user,
                                                   'source':source,
                                                   'service':service,
                                                   })



@method_decorator(login_required, name="dispatch")
class AmcListView(generic.ListView):
    """
    View for listing AMC (Annual Maintenance Contract) instances.

    Attributes:
        model: The model used by the ListView (Amc).
        template_name: The name of the template to render the list view.

    Methods:
        get_context_data(self, **kwargs): Overrides the default method 
                                          to provide additional context data.

    """
    model=Amc
    template_name = 'amc/amc_list.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves and provides additional context data for rendering the template.

        Returns:
            dict: A dictionary containing context data.

        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_service_admin or self.request.user.is_service_agent or self.request.user.is_superuser: # pylint: disable=line-too-long
            context["amc"] = Amc.objects.all() # pylint: disable=no-member
        else:
            context['amc']= Amc.objects.filter(company=self.request.user.user_company) # pylint: disable=no-member
        return context


@login_required
def amc_detail(request, pk):
    """
    View for displaying details of a specific AMC (Annual Maintenance Contract) instance.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the AMC instance.

    Returns:
        HttpResponse: The HTTP response object containing the AMC details.

    Raises:
        Amc.DoesNotExist: If the specified AMC instance does not exist.
        Company.DoesNotExist: If the company associated with the AMC instance does not exist.
        Http404: If the user does not have permission to access the AMC instance.

    """
    amc_pk =Amc.objects.get(id=pk) # pylint: disable=no-member
    company= Company.objects.get(pk=amc_pk.company.pk) # pylint: disable=no-member

    if request.user.is_customer_user and request.user.is_customer_admin:
        products=Product.objects.filter(amc_id=amc_pk).order_by('location') # pylint: disable=no-member
    elif request.user.is_customer_user:
        products=Product.objects.filter(amc_id=amc_pk).filter(location=request.user.user_loc).order_by('location') # pylint: disable=no-member line-too-long
    else:
        products=Product.objects.filter(amc_id=amc_pk).order_by('location') # pylint: disable=no-member
    amc_value = products.aggregate(amc_value = Sum('amount'))

    context = {
        "amc": amc_pk,
        "company":company,
        "products":products,
        "amc_value":amc_value,
    }
    return render(request, 'amc/amc_detail.html', context)


@method_decorator(login_required, name="dispatch")
class AmcUpdateView(generic.UpdateView):
    """
    View for updating an existing AMC (Annual Maintenance Contract) instance.

    Attributes:
        model: The model used by the UpdateView (Amc).
        form_class: The form class used for updating the AMC instance (CreateAmcForm).
        template_name: The name of the template to render the update view.

    Methods:
        get_success_url(self): Overrides the default method to return the URL 
        to redirect to after a successful update.

    """
    model = Amc
    form_class = CreateAmcForm
    template_name = 'Amc_update.html'

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful update.

        Returns:
            str: The URL to redirect to (AmcList).

        """
        return reverse('AmcList')

@login_required
def load_contact_person(request):
    """
    View for retrieving contact persons associated with a product's location.

    This view is intended to be called asynchronously via AJAX.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing contact person details.

    Raises:
        Product.DoesNotExist: If the specified product does not exist.
        ValueError: If the 'product_id' parameter is missing or invalid.

    """
    if request.method == "GET":
        product_id = request.GET.get('product_id')
        print(product_id)
        prod=Product.objects.get(pk=product_id) # pylint: disable=no-member
        print(prod.location)

        # Assuming User model has a field 'user_loc' that matches the product_id
        user_details = User.objects.filter(user_loc=prod.location.id).values()
        # Customize the fields you want to retrieve from the User model
        print(user_details)
        # Convert queryset to list of dictionaries for JSON serialization
        user_details_list = list(user_details)

        return JsonResponse({'user_detail': user_details_list})

    return JsonResponse({'error': 'Invalid request'}, status=400)



# def create_amc(request,pk):
#     companies=Company.objects.get(id=pk)
#     print(companies.company_name)
#     # companies=Company.objects.all()
#     locations= Location.objects.filter(loc_company_id=companies)
#     # locations= Location.objects.all()
#     products= Product.objects.all()
#     form = CreateAmcForm(request.POST)
#     if form.is_valid():
#         print("form is okay")
#         # form.save()
#         var = form.save(commit=False)
#         var.company= companies
#         # var.location= location
#         # var.user= request.user
#         var.save()
#         return redirect('AmcList')
#     else:print("form not okay")
#     context = {
#         'form':form,
#         'companies':companies,
#         'locations':locations,
#         'products':products,
#     }
#     return render(request,'amc/amc_create.html',context)
