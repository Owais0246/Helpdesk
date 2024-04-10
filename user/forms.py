from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from masters.models import Company, Location
class CreateUser(UserCreationForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'username', 'user_contact_no', 'email','is_customer_admin','password1','password2' ]
        
class CreateUserNew(forms.ModelForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'user_contact_no', 'email','is_customer_admin', 'is_customer_user' ]
# class UpdateUser(forms.Form):
#     class Meta:
#         model=User 
#         fields= ['first_name', 'last_name',  'email','password1','password2','user_company','user_loc','user_contact_no' ]


class ServiceAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'user_contact_no','email','aadhaar_no','covid_cert','password1','password2',]


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_contact_no','email','aadhaar_no','covid_cert']
        
        
class salesForm(UserCreationForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.none(),  # Initially an empty queryset
        required=True,
        label='Location',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'user_contact_no', 'email', 'aadhaar_no', 'covid_cert', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(salesForm, self).__init__(*args, **kwargs)

        # Update the queryset for the location field based on the company with is_self_company=True
        company = Company.objects.filter(is_self_company=True).first()
        if company:
            self.fields['location'].queryset = Location.objects.filter(loc_company=company)
            

class salesUpdateForm(UserCreationForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.none(),  # Initially an empty queryset
        required=True,
        label='Location',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_contact_no', 'email']

    def __init__(self, *args, **kwargs):
        super(salesUpdateForm, self).__init__(*args, **kwargs)

        # Update the queryset for the location field based on the company with is_self_company=True
        company = Company.objects.filter(is_self_company=True).first()
        if company:
            self.fields['location'].queryset = Location.objects.filter(loc_company=company)