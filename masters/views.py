from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import CompanyForm,LocationForm,ProductForm
from django.views import generic
from . models import Company,Location,Product
# Create your views here.

#Company Views

def CreateCustomer(request):
    pass
class CustomerCreateView(generic.CreateView):
    template_name = 'masters/company/company_create.html'
    form_class = CompanyForm

    def get_success_url(self):
        return reverse('CompanyList')

class CustomerListView(generic.ListView):
    template_name = 'masters/company/company_list.html'
    queryset = Company.objects.all()
    context_object_name = 'company'

def CustomerDetail(request, pk):
    company_pk =Company.objects.get(id=pk)

    context = {
        "company": company_pk,
    }
    return render(request, 'masters/company/company_detail.html', context)



class CustomerUpdateView(generic.UpdateView):
    model =Company
    form_class = CompanyForm
    template_name = 'masters/company/company_update.html'

    def get_success_url(self):
        return reverse('CompanyList')


#Location Views
class LocationCreateView(generic.CreateView):
    template_name = 'masters/location/location_create.html'
    form_class = LocationForm

    def get_success_url(self):
        return reverse('LocationList')

class LocationListView(generic.ListView):
    template_name = 'masters/location/location_list.html'
    queryset = Location.objects.all()
    context_object_name = 'location'



def LocationDetail(request, pk):
    location_pk =Location.objects.get(id=pk)

    context = {
        "location": location_pk,
    }
    return render(request, 'masters/location/location_detail.html', context)



class LocationUpdateView(generic.UpdateView):
    model =Location
    form_class = LocationForm
    template_name = 'masters/location/location_update.html'

    def get_success_url(self):
        return reverse('LocationList')
    
    
#Product Views
class ProductCreateView(generic.CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('ProductList')

class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    queryset = Product.objects.all()
    context_object_name = 'product'


def ProductDetail(request, pk):
    product_pk =Product.objects.get(id=pk)

    context = {
        "product": product_pk,
    }
    return render(request, 'product/product_detail.html', context)

class ProductUpdateView(generic.UpdateView):
    model =Product
    form_class =ProductForm
    template_name = 'product/product_update.html'

    def get_success_url(self):
        return reverse('ProductList')