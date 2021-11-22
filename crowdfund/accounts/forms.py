from django import forms
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    phone_number = PhoneNumberField(
    widget=PhoneNumberPrefixWidget(initial='EG')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone_number', 'profile_picture')

