from django import forms
from .models import Amc


class CreateAmcForm(forms.ModelForm):
    class Meta:
        model = Amc
        fields = ('location','product','start_date',
                  'expiry','description','sla','escalation_matrix_1','escalation_matrix_2','escalation_matrix_3','escalation_matrix_4')
        # 
        # labels = {
        #     'loc_name': 'Location Name',
        #     'loc_company': 'Company',
        #     'loc_poc_contact_no': 'POC\'s Phone Number',
        #     'loc_address': 'Address',

        # }
        
        