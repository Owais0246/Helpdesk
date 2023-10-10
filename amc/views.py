from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import CreateAmcForm, ProductForm, AmcForm, ProductFormSet
from django.views import generic
from . models import Amc
from masters.models import Company,Location,Product
from user.models import User
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

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

def create_amc(request, pk):
    company=Company.objects.get(id=pk)
    locations=Location.objects.filter(loc_company=company)
    products_formset = ProductFormSet(request.POST)
    if request.method == 'POST':
        amc_form = AmcForm(request.POST)
        if amc_form.is_valid():
            print("Amc  valid")
            amc1 = amc_form.save(commit=False)
            amc1.company= company
            amc=amc1.save()
            
            # Process product formset data
            products_formset = ProductFormSet(request.POST)
            if products_formset.is_valid():
                print("Product  valid")
                for product_form in products_formset:
                    product_name = product_form.cleaned_data.get('product_name')
                    part_number = product_form.cleaned_data.get('part_number')
                    serial_number = product_form.cleaned_data.get('serial_number')
                    description = product_form.cleaned_data.get('description')
                    location = product_form.cleaned_data.get('location')
                    
                    print(product_name)
                    print(part_number)
                    print(serial_number)
                    print(description)
                    print(location)

  
     
                    
                    # Save product data related to the AMC
                    Product.objects.create(
                        product_name=product_name,
                        part_number=part_number,
                        serial_number=serial_number,
                        description=description,
                        location=location,
                        amc=amc
                    )
                    
                # Redirect or do something else after successful form submission
                return redirect('/')
    else:
        amc_form = AmcForm()
        products_formset = ProductFormSet()

    return render(request, 'amc/amc_create.html', {'amc_form': amc_form, 'products_formset': products_formset,'company':company,'locations':locations})





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

class AmcListView(generic.ListView):
    template_name = 'amc/amc_list.html'
    queryset = Amc.objects.all()
    context_object_name = 'amc'



def AmcDetail(request, pk):
    amc_pk =Amc.objects.get(id=pk)

    context = {
        "amc": amc_pk,
    }
    return render(request, 'amc/amc_detail.html', context)



class AmcUpdateView(generic.UpdateView):
    model = Amc
    form_class = CreateAmcForm
    template_name = 'Amc_update.html'

    def get_success_url(self):
        return reverse('AmcList')


