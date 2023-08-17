from django import forms
from .models import Amc


      

class CreateAmcForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ('company','location','user','product_name',
                  'startdate','duration','part_number','serial_number','description',)
        # labels = {
        #     'loc_name': 'Location Name',
        #     'loc_company': 'Company',
        #     'loc_poc_contact_no': 'POC\'s Phone Number',
        #     'loc_address': 'Address',

        # }