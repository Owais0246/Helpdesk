from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import AmcForm
from django.views import generic
from . models import Amc
# Create your views here.

#AMC Views
class AmcCreateView(generic.CreateView):
    template_name = 'amc/amc_create.html'
    form_class = AmcForm

    def get_success_url(self):
        return reverse('AmcList')

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
    form_class = AmcForm
    template_name = 'Amc_update.html'

    def get_success_url(self):
        return reverse('AmcList')


