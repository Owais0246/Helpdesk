from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUser(UserCreationForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'username', 'user_contact_no', 'email','is_customer_admin','password1','password2' ]
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