from django import forms
from django.forms.widgets import NumberInput
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)
    phone_number = PhoneNumberField(
    widget=PhoneNumberPrefixWidget(initial='EG'), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone_number', 'profile_picture')


class ProfileUpdateForm(forms.ModelForm):

    phone_number = PhoneNumberField(
    widget=PhoneNumberPrefixWidget(initial='EG'), required=False)
    birth_date = forms.DateField(label="Birth Date", required=False,
     widget=NumberInput(attrs={'type':'date'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'profile_picture', 'birth_date', 'country', 'facebook')


class LoginForm(AuthenticationForm):

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password"),
        'inactive': _("Please activate the account to sign in"),}

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except:
                    user_temp = None

                if user_temp is not None and user_temp.check_password(password):
                    self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data