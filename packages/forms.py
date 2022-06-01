from packages.models import Packages
from django import forms

class PackagesForm(forms.ModelForm):
    class Meta:
        model= Packages
        fields=['packagess_name','destination_List','description','price','rating','image','cover_pick','event']
