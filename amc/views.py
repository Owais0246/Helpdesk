from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import CreateAmcForm
from django.views import generic
from . models import Amc
from masters.models import Company,Location,Product
from user.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

#AMC Views

def create_amc(request):
    companies=Company.objects.all()
    locations= Location.objects.all()
    products= Product.objects.all()
    form = CreateAmcForm(request.POST)
    if form.is_valid():
        print("form is okay")
        form.save()
        # var = form.save(commit=False)
        # var.company= company
        # var.location= location
        # var.user= request.user
        # var.save()
        return redirect('AmcList')
    else:print("form not okay")
    context = {
        'form':form,
        'companies':companies,
        'locations':locations,
        'products':products,
        
    }
    return render(request,'amc/amc_create.html',context)

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


