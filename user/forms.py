from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUser(UserCreationForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'username', 'user_email','password1','password2','user_contact_no' ]
class UpdateUser(forms.ModelForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name',  'email','password1','password2','user_company','user_loc','user_contact_no' ]