from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUser(UserCreationForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'username', 'email','password1','password2','user_contact_no','is_customer_admin' ]
# class UpdateUser(forms.Form):
#     class Meta:
#         model=User 
#         fields= ['first_name', 'last_name',  'email','password1','password2','user_company','user_loc','user_contact_no' ]


class ServiceAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email','password1','password2','user_contact_no','aadhaar_no','covid_cert']


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','user_contact_no','aadhaar_no','covid_cert']