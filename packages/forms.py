from packages.models import Packages
from django import forms

class PackagesForm(forms.ModelForm):
    class Meta:
        model= Packages
        fields="__all__"
