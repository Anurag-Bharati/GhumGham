from django import forms
from dashboard.models import Package, Place, Adventure, Food, Itinerary, Order
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


class CreatePlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'name', 'coordinate', 'adventures', 'food',
            'image', 'cover_image', 'date_time',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'required': '',
            'name': 'name',
            'id': 'name',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Place Name',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['coordinate'].widget.attrs.update({
            'required': '',
            'name': 'coordinate',
            'id': 'coordinate',
            'type': 'number',
            'class': 'form-control form-control-user',
            'placeholder': 'Place Coordinate',
        })
        self.fields['adventures'].widget.attrs.update({
            'required': '',
            'name': 'adventures',
            'id': 'adventures',
            'class': 'form-control form-control-user',
        })
        self.fields['food'].widget.attrs.update({
            'required': '',
            'name': 'food',
            'id': 'food',
            'class': 'form-control form-control-user',
        })

        self.fields['date_time'].widget = forms.DateTimeInput(attrs={
            'name': 'date_time',
            'id': 'date_time',
            'type': 'datetime-local',
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


class CreateAdventureForm(forms.ModelForm):
    class Meta:
        model = Adventure
        fields = [
            'name', 'adventure'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'required': '',
            'name': 'name',
            'id': 'name',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Name of the adventure',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['adventure'].widget.attrs.update({
            'required': '',
            'name': 'adventure',
            'id': 'adventure',
            'type': 'select',
            'class': 'form-control form-control-user',
        })


class CreateItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = [
            'name', 'duration', 'places'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'required': '',
            'name': 'name',
            'id': 'name',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Name of the Itinerary',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['places'].widget.attrs.update({
            'required': '',
            'name': 'places',
            'id': 'places',
            'class': 'form-control form-control-user',
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


class CreateFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'name', 'breakfast', 'lunch', 'snacks', 'dinner'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'required': '',
            'name': 'name',
            'id': 'name',
            'type': 'text',
            'class': 'form-control form-control-user',
            'placeholder': 'Name of the Food Stop',
            'maxlength': '50',
            'minlength': '3',
        })
        self.fields['breakfast'].widget.attrs.update({
            'name': 'breakfast',
            'id': 'breakfast',
            'class': 'form-control form-control-user',
        })
        self.fields['lunch'].widget.attrs.update({
            'name': 'lunch',
            'id': 'lunch',
            'class': 'form-control form-control-user',
        })
        self.fields['snacks'].widget.attrs.update({
            'name': 'snacks',
            'id': 'snacks',
            'class': 'form-control form-control-user',
        })
        self.fields['dinner'].widget.attrs.update({
            'name': 'dinner',
            'id': 'dinner',
            'class': 'form-control form-control-user',
        })


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'customer_phone', 'staff', 'package', 'date', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'].widget.attrs.update({
            'required': '',
            'class': 'form-control form-control-user',
        })

        self.fields['package'].widget.attrs.update({
            'required': '',
            'class': 'form-control form-control-user',
        })

        self.fields['staff'].widget.attrs.update({
            'class': 'form-control form-control-user',
        })

        self.fields['status'].widget.attrs.update({
            'required': '',
            'class': 'form-control form-control-user',
        })
        self.fields['date'].widget = forms.DateTimeInput(attrs={
            'name': 'date',
            'id': 'date',
            'type': 'date',
            'class': 'form-control form-control-user',
        })

        self.fields['customer_phone'].widget.attrs.update({
            'required': '',
            'name': 'phone',
            'id': 'phone',
            'type': 'tel',
            'class': 'form-control form-control-user',
            'placeholder': 'Phone of the user',
        })


class CreateUserForm(forms.ModelForm):
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
            'placeholder': 'Address of the user',
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
