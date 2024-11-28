from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Partner, Region, State, City
from .forms import PartnerForm, LocationForm
from django.views.generic import ListView

# Create a Partner
def partner_create(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partner_list')  # Redirect to a page where partners are listed (you can define this view)
    else:
        form = PartnerForm()

    return render(request, 'partner/partner_create.html', {'form': form})

def partner_detail(request, partner_id):
    # Fetch the partner by ID
    partner = Partner.objects.get(id=partner_id)

    # Retrieve engineers related to this partner
    engineers = partner.engineers.all()

    # For each engineer, get their associated regions
    engineer_locations = []
    for engineer in engineers:
        regions = engineer.engineerlocation_set.all()  # Get regions for the engineer
        engineer_locations.append({
            'engineer': engineer,
            'regions': [location.region for location in regions]  # Get regions from EngineerLocation
        })

    return render(
        request,
        'partner/partner_detail.html',
        {
            'partner': partner,
            'engineer_locations': engineer_locations
        }
    )

# List Partners (optional)
def partner_list(request):
    partners = Partner.objects.all()
    return render(request, 'partner/partner_list.html', {'partners': partners})


def location_create_view(request):
    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # Save the location or take further action
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            region = form.cleaned_data['region']
            # Optionally, save them in their respective models
            return redirect('location_list')  # Redirect after success
    return render(request, 'partner/location_create.html', {'form': form})

def get_states(request):
    # Get all states from the database
    states = State.objects.all().values('id', 'name')
    return JsonResponse(list(states), safe=False)

def get_cities(request):
    state_name = request.GET.get('state', '')
    state = State.objects.filter(name__icontains=state_name).first()
    if state:
        cities = City.objects.filter(state=state).values('id', 'name')
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([])

def get_regions(request):
    city_name = request.GET.get('city', '')
    city = City.objects.filter(name__icontains=city_name).first()
    if city:
        regions = Region.objects.filter(city=city).values('id', 'name')
        return JsonResponse(list(regions), safe=False)
    return JsonResponse([])



def location_list(request):
    # Fetching all the regions along with related cities and states
    regions = Region.objects.all().select_related('city__state')
    
    # Passing the regions to the template
    return render(request, 'partner/location_list.html', {'regions': regions})

def edit_location(request, region_id):
    # Get the region object based on the provided region_id
    region = get_object_or_404(Region, pk=region_id)
    
    if request.method == 'POST':
        # Create a form instance with POST data and the existing instance
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            # Save the form to update the region
            form.save()
            return redirect('location_list')  # Redirect to the location list after saving
    else:
        # Pre-fill the form with existing region data
        form = RegionForm(instance=region)
    
    return render(request, 'partner/edit_location.html', {'form': form, 'region': region})