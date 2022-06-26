from django import forms
from dashboard.models import Package
from users.models import User


class CreatePackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'name', 'type', 'itinerary', 'price',
            'image', 'cover_image', 'desc', 'duration', 'status', 'is_featured',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'required': '',
            'name': 'name',
            'id': 'name',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Package Name',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['type'].widget.attrs.update({
            'required': '',
            'name': 'type',
            'id': 'type',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Package Type',
        })
        self.fields['itinerary'].widget.attrs.update({
            'required': '',
            'name': 'itinerary',
            'id': 'itinerary',
            'class': 'form-control form-control-user',

        })
        self.fields['desc'].widget = forms.Textarea(attrs={
            'required': '',
            'name': 'desc',
            'id': 'desc',
            'type': 'textarea',
            'class': 'form-control form-control-user',
            'placeholder': 'A short description',
            'maxlength': '500',
            'minlength': '3',
            'rows': '5', })

        self.fields['price'].widget.attrs.update({
            'name': 'price',
            'id': 'price',
            'type': 'number',
            'class': 'form-control form-control-user',
            'placeholder': 'In dollar(s)',
            'max': '1000',
            'min': '1',
        })
        self.fields['duration'].widget.attrs.update({
            'required': '',
            'name': 'duration',
            'id': 'duration',
            'type': 'number',
            'class': 'form-control form-control-user',
            'placeholder': 'In day(s)',
            'max': '100',
            'min': '1',
        })
        self.fields['image'].widget.attrs.update({
            'name': 'image',
            'id': 'image',
            'type': 'file',
            'class': 'form-control form-control-user',
        })

        self.fields['cover_image'].widget.attrs.update({
            'name': 'cover_image',
            'id': 'cover_image',
            'type': 'file',
            'class': 'form-control form-control-user',
        })


class CreateStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'address', 'image', 'password',
            'cover_image', 'is_active', 'is_ban'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Name of Staff',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['email'].widget.attrs.update({
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control form-control-user',
            'placeholder': 'Email of staff',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'required': '',
            'name': 'password',
            'id': 'password',
            'type': 'password',
            'class': 'form-control form-control-user',
            'placeholder': '********',
        })
        self.fields['address'].widget.attrs.update({
            'required': '',
            'name': 'address',
            'id': 'address',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Address of staff',
        })
        self.fields['is_active'].widget = forms.NullBooleanSelect(attrs={
            'required': '',
            'name': 'is_active',
            'id': 'is_active',
            'class': 'form-control form-control-user',
        })
        self.fields['is_ban'].widget = forms.NullBooleanSelect(attrs={
            'required': '',
            'name': 'is_ban',
            'id': 'is_ban',
            'class': 'form-control form-control-user',
        })
        self.fields['image'].widget.attrs.update({
            'name': 'image',
            'id': 'image',
            'type': 'file',
            'class': 'form-control form-control-user',
        })

        self.fields['cover_image'].widget.attrs.update({
            'name': 'cover_image',
            'id': 'cover_image',
            'type': 'file',
            'class': 'form-control form-control-user',
        })
