from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Partner, Region, State, City
from .forms import PartnerForm, LocationForm, EngineerForm
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
    partner = Partner.objects.get(id=partner_id)
    
    # Fetch engineers for this partner, including their associated regions
    engineers = partner.engineers.all()

    # Use distinct() to get unique regions
    regions = set()
    for engineer in engineers:
        for region in engineer.region.all():
            regions.add(region)  # Use a set to ensure unique regions

    return render(request, 'partner/partner_detail.html', {
        'partner': partner,
        'engineers': engineers,
        'regions': regions,  # Pass unique regions here
    })
# List Partners (optional)
def partner_list(request):
    partners = Partner.objects.all()
    return render(request, 'partner/partner_list.html', {'partners': partners})


def location_create_view(request):
    if request.method == "POST":
        # Handling form submission
        form = LocationForm(request.POST)
        if form.is_valid():
            state_name = form.cleaned_data['state']
            city_name = form.cleaned_data['city']
            region_name = form.cleaned_data['region']
            pin_code = form.cleaned_data['pin']
            
            # Create or get State, City, and Region
            state, created = State.objects.get_or_create(name=state_name)
            city, created = City.objects.get_or_create(name=city_name, state=state)
            region, created = Region.objects.get_or_create(name=region_name, city=city, pin=pin_code)
            
            return redirect('location_list')

    else:
        form = LocationForm()

    return render(request, "partner/location_create.html", {"form": form})

# AJAX Views

def get_states(request):
    query = request.GET.get('q', '')
    states = State.objects.filter(name__icontains=query)
    suggestions = [state.name for state in states]
    return JsonResponse({'suggestions': suggestions})

def get_cities(request):
    query = request.GET.get('q', '')
    state_id = request.GET.get('state_id', None)
    if state_id:
        cities = City.objects.filter(state_id=state_id, name__icontains=query)
    else:
        cities = City.objects.filter(name__icontains=query)
    suggestions = [city.name for city in cities]
    return JsonResponse({'suggestions': suggestions})

def get_regions(request):
    query = request.GET.get('q', '')
    city_id = request.GET.get('city_id', None)
    if city_id:
        regions = Region.objects.filter(city_id=city_id, name__icontains=query)
    else:
        regions = Region.objects.filter(name__icontains=query)
    suggestions = [region.name for region in regions]
    return JsonResponse({'suggestions': suggestions})


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





def create_engineer(request, partner_id):
    """
    View for creating an engineer and associating them with regions.
    The partner_id is passed via the URL to associate the engineer with a specific partner.
    """
    partner = get_object_or_404(Partner, id=partner_id)  # Fetch the partner object
    
    if request.method == 'POST':
        form = EngineerForm(request.POST)
        if form.is_valid():
            # Set the partner to the form instance before saving
            engineer = form.save(commit=False)  # Don't save yet
            engineer.partner = partner  # Associate the engineer with the partner
            engineer.save()  # Now save the engineer

            # Associate selected regions (ManyToMany relationship)
            for region in form.cleaned_data['region']:  # Use 'region' instead of 'regions'
                engineer.region.add(region)  # Add the region to the engineer

            return redirect('partner_detail', partner_id=partner.id)  # Redirect to a list of engineers (or wherever you need)
        else:
            print("Form is not valid:", form.errors)  # Debug: print errors if the form is not valid
    else:
        form = EngineerForm()

    return render(request, 'partner/create_engineer.html', {'form': form, 'partner': partner})

    # return render(request, 'partner/create_engineer.html', {'form': form, 'partner': partner})
    # return render(request, 'partner/create_engineer.html', {'form': form})
    
    
def state_detail(request, state_id):
    """
    State detail view that shows all the engineers and partners
    associated with a particular state, along with cities and regions.
    """
    state = get_object_or_404(State, id=state_id)
    
    # Get all cities associated with the state
    cities = state.cities.all()
    
    # Collect all engineers and partners for each city and region
    partners = []
    engineers = []
    for city in cities:
        for region in city.regions.all():
            for engineer in region.engineer_set.all():
                engineers.append(engineer)
                partners.append(engineer.partner)
    
    # Get unique partners and engineers
    partners = list(set(partners))
    engineers = list(set(engineers))
    
    return render(request, 'partner/state_detail.html', {
        'state': state,
        'partners': partners,
        'engineers': engineers,
        'cities': cities,
    })

def city_detail(request, city_id):
    """
    City detail view that shows all the engineers and partners
    associated with a particular city, along with regions and pin codes.
    """
    city = get_object_or_404(City, id=city_id)
    
    # Get all regions associated with the city
    regions = city.regions.all()
    
    # Collect all engineers and partners for each region
    partners = []
    engineers = []
    for region in regions:
        for engineer in region.engineer_set.all():
            engineers.append(engineer)
            partners.append(engineer.partner)
    
    # Get unique partners and engineers
    partners = list(set(partners))
    engineers = list(set(engineers))
    
    return render(request, 'partner/city_detail.html', {
        'city': city,
        'partners': partners,
        'engineers': engineers,
        'regions': regions,
    })
    

def region_detail(request, region_id):
    """
    Region detail view that shows all the engineers and partners
    associated with a particular region.
    """
    region = get_object_or_404(Region, id=region_id)
    
    # Get all engineers who serve this region
    engineers = region.engineer_set.all()
    
    # Collect the partners of the engineers
    partners = [engineer.partner for engineer in engineers]
    
    return render(request, 'partner/region_detail.html', {
        'region': region,
        'partners': partners,
        'engineers': engineers,
    })