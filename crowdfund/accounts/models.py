from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField



class User(AbstractUser):
    
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    date_joined = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(default='avatar.png', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
