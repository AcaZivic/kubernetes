from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

# - Register/Create a user

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']


# - Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Create a Customer

class CreateCustomerForm(forms.ModelForm):

    class Meta:

        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'country']


# - Update a Customer

class UpdateCustomerForm(forms.ModelForm):

    class Meta:

        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'country']
