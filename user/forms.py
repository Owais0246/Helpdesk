from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUser(UserCreationForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'username', 'user_type', 'email','password1','password2','user_company','user_loc','contact_no' ]
class UpdateUser(forms.ModelForm):
    class Meta:
        model=User 
        fields= ['first_name', 'last_name', 'user_type', 'email','password1','password2','user_company','user_loc','contact_no' ]