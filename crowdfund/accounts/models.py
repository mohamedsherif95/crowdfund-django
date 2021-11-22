from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField



class User(AbstractUser):
    
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(blank=True)
    profile_picture = models.ImageField(null=True, default='avatar.png')
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
