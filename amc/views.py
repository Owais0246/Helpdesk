from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import CreateAmcForm, ProductForm, AMCForm, ProductFormSet
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
    location=Location.objects.filter(loc_company=company)
    
    if request.method == 'POST':
        amc_form = AMCForm(request.POST)
        product_formset = ProductFormSet(request.POST, instance=Amc(company=company))

        if amc_form.is_valid() and product_formset.is_valid():
            amc_instance = amc_form.save(commit=False)
            amc_instance.company = company  # Assign the company to the AMC instance
            amc_instance.save()
            product_formset.instance = amc_instance
            product_formset.save()

            # Redirect or do something else after successful form submission
            return redirect('CompanyDetail', pk)  # Replace '/success/' with your success URL
    else:
        amc_form = AMCForm()
        product_formset = ProductFormSet(instance=Amc(company=company))
    return render(request, 'amc/amc_create.html', {'amc_form': amc_form, 'product_formset': product_formset, 'location':location, 'company':company})

    # return render(request, 'amc/amc_create.html', {'amc_form': amc_form, 'products_formset': products_formset,'company':company,'locations':locations})





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


