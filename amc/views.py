from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import CreateAmcForm, ProductForm, AMCForm, ProductFormSet
from django.views import generic
from . models import Amc
from masters.models import Company,Location,Product
from user.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

#AMC Views
# Amc creation old view
# def create_amc(request):
#     companies=Company.objects.all()
#     locations= Location.objects.all()
#     products= Product.objects.all()
#     form = CreateAmcForm(request.POST)
#     if form.is_valid():
#         print("form is okay")
#         form.save()
#         # var = form.save(commit=False)
#         # var.company= company
#         # var.location= location
#         # var.user= request.user
#         # var.save()
#         return redirect('AmcList')
#     else:print("form not okay")
#     context = {
#         'form':form,
#         'companies':companies,
#         'locations':locations,
#         'products':products,
        
#     }
#     return render(request,'amc/amc_create.html',context)

# Amc creation new view

# def create_amc(request, pk):
#     company=Company.objects.get(id=pk)
#     # location=Location.objects.filter(loc_company=company)
#     location=Location.objects.all()
    
    
#     if request.method == 'POST':
#         amc_form = AMCForm(request.POST)
#         product_formset = ProductFormSet(request.POST, instance=Amc(company=company))

#         if amc_form.is_valid() and product_formset.is_valid():
#             amc_instance = amc_form.save(commit=False)
#             amc_instance.company = company  # Assign the company to the AMC instance
#             amc_instance.save()
#             product_formset.instance = amc_instance
#             product_formset.save()

#             # Redirect or do something else after successful form submission
#             return redirect('CompanyDetail', pk)  # Replace '/success/' with your success URL
#     else:
#         amc_form = AMCForm()
#         product_formset = ProductFormSet(instance=Amc(company=company))
#     return render(request, 'amc/amc_create.html', {'amc_form': amc_form, 'product_formset': product_formset, 'locations':location, 'company':company})

    # return render(request, 'amc/amc_create.html', {'amc_form': amc_form, 'products_formset': products_formset,'company':company,'locations':locations})



@login_required
def create_amc(request, pk):
    company = Company.objects.get(id=pk)
    location = Location.objects.filter(loc_company=company)  # Retrieve location data

    ProductFormSet = inlineformset_factory(Amc, Product, form=ProductForm, extra=1)

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
            return redirect('CompanyDetail', pk)  # Replace 'CompanyDetail' with your success URL name

    else:
        amc_form = AMCForm()
        product_formset = ProductFormSet(instance=Amc(company=company))

    return render(request, 'amc/amc_create.html', {'amc_form': amc_form, 'product_formset': product_formset, 'locations': location, 'company': company})




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

@method_decorator(login_required, name="dispatch")
class AmcListView(generic.ListView):
    model=Amc
    template_name = 'amc/amc_list.html'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        if self.request.user.is_service_admin or self.request.user.is_service_agent or self.request.user.is_superuser:
            context["amc"] = Amc.objects.all()
        else:
            context['amc']= Amc.objects.filter(company=self.request.user.user_company)
        return context
    
@login_required  
def AmcDetail(request, pk):
    amc_pk =Amc.objects.get(id=pk)
    company= Company.objects.get(pk=amc_pk.company.pk)
    
    if request.user.is_customer_user and request.user.is_customer_admin:
        products=Product.objects.filter(amc_id=amc_pk).order_by('location')
    elif request.user.is_customer_user:
        products=Product.objects.filter(amc_id=amc_pk).filter(location=request.user.user_loc).order_by('location')
    else: 
        products=Product.objects.filter(amc_id=amc_pk).order_by('location')
        
    
    

    context = {
        "amc": amc_pk,
        "company":company,
        "products":products
    }
    return render(request, 'amc/amc_detail.html', context)


@method_decorator(login_required, name="dispatch")
class AmcUpdateView(generic.UpdateView):
    model = Amc
    form_class = CreateAmcForm
    template_name = 'Amc_update.html'

    def get_success_url(self):
        return reverse('AmcList')

@login_required
def load_contact_person(request):
    if request.method == "GET":
        product_id = request.GET.get('product_id')
        print(product_id)
        prod=Product.objects.get(pk=product_id)
        print(prod.location)
        
        # Assuming User model has a field 'user_loc' that matches the product_id
        user_details = User.objects.filter(user_loc=prod.location.id).values()
        # Customize the fields you want to retrieve from the User model
        print(user_details)
        # Convert queryset to list of dictionaries for JSON serialization
        user_details_list = list(user_details)
        
        return JsonResponse({'user_detail': user_details_list})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



