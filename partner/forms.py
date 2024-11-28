"""
Django forms for managing Partner, Engineer, Location (State, City, Region), 
and EngineerLocation models.

This module defines the following forms:
- PartnerForm: A form for managing partner data.
- EngineerForm: A form for managing engineer data.
- LocationForm: A form for managing location data (State, City, Region).
- EngineerLocationForm: A form for assigning engineers to regions.
"""
from django import forms
from .models import Partner, Engineer, State, City, Region, EngineerLocation

# Form for Partner
class PartnerForm(forms.ModelForm):
    """
    Form to create or update a partner.
    """
    class Meta:
        model = Partner
        fields = ['name', 'contact_name', 'email_address', 'contact_no']
        widgets = {
            'contact_no': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Enter email address'})
        }

# Form for Engineer
# class EngineerForm(forms.ModelForm):
#     """
#     Form to create or update an engineer associated with a partner.
#     """
#     class Meta:
#         model = Engineer
#         fields = ['partner', 'name', 'email', 'contact_no', 'expertise']
#         widgets = {
#             'contact_no': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
#             'expertise': forms.Textarea(attrs={'placeholder': 'Enter expertise details'}),
#         }

# # Form for State
# class StateForm(forms.ModelForm):
#     """
#     Form to create or update a state.
#     """
#     class Meta:
#         model = State
#         fields = ['name']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter state name'}),
#         }

# # Form for City
# class CityForm(forms.ModelForm):
#     """
#     Form to create or update a city.
#     """
#     state = forms.ModelChoiceField(queryset=State.objects.all(), required=True)

#     class Meta:
#         model = City
#         fields = ['state', 'name']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter city name'}),
#         }

# # Form for Region
# class RegionForm(forms.ModelForm):
#     """
#     Form to create or update a region.
#     """
#     city = forms.ModelChoiceField(queryset=City.objects.all(), required=True)

#     class Meta:
#         model = Region
#         fields = ['city', 'name']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Enter region name'}),
#         }

# # Form for EngineerLocation (Assigning an engineer to a region)
# class EngineerLocationForm(forms.ModelForm):
#     """
#     Form to create or update the relationship between an engineer and a region.
#     """
#     engineer = forms.ModelChoiceField(queryset=Engineer.objects.all(), required=True)
#     region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True)

#     class Meta:
#         model = EngineerLocation
#         fields = ['engineer', 'region']
    
#     def clean(self):
#         """
#         Custom validation to ensure that a given engineer is not already assigned to the same region.
#         """
#         cleaned_data = super().clean()
#         engineer = cleaned_data.get('engineer')
#         region = cleaned_data.get('region')
        
#         if EngineerLocation.objects.filter(engineer=engineer, region=region).exists():
#             raise forms.ValidationError(f"{engineer.name} is already assigned to this region.")
        
#         return cleaned_data


class LocationForm(forms.Form):
    state = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    region = forms.CharField(max_length=100, required=True)

    def clean_state(self):
        state_name = self.cleaned_data.get('state')
        state, created = State.objects.get_or_create(name=state_name)
        return state

    def clean_city(self):
        city_name = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        if state:
            city, created = City.objects.get_or_create(name=city_name, state=state)
            return city
        return None

    def clean_region(self):
        region_name = self.cleaned_data.get('region')
        city = self.cleaned_data.get('city')
        if city:
            region, created = Region.objects.get_or_create(name=region_name, city=city)
            return region
        return None
    
class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'city']  # Include state, city, and region name in the form
