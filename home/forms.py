from django import forms

from users.models import User


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'address', 'image', 'cover_image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Name of the user',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['email'].widget.attrs.update({
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control form-control-user',
            'placeholder': 'Email of the user',
        })
        self.fields['address'].widget.attrs.update({
            'required': '',
            'name': 'address',
            'id': 'address',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Address of the user',
        })
        self.fields['image'].widget.attrs.update({
            'name': 'image',
            'id': 'image',
            'type': 'file',
            'class': 'form-control-file',
        })

        self.fields['cover_image'].widget.attrs.update({
            'name': 'cover_image',
            'id': 'cover_image',
            'type': 'file',
            'class': 'form-control-file',
        })
