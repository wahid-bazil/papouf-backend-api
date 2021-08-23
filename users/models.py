from delivery.models import ShippingCity
from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, second_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, second_name, password, **other_fields)

    def create_user(self, email, name, second_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          second_name=second_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150, null=False)
    second_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15 , blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'second_name']

    def __str__(self):
        return self.email

    @property
    def client_email(self):
        return self.email
        
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class Address(models.Model):
    user = models.OneToOneField(NewUser,related_name="address_details", on_delete=models.CASCADE,primary_key=True )
    city = models.ForeignKey(ShippingCity,on_delete=models.SET_NULL ,null=True ,blank=True)
    address = models.CharField(max_length=100, blank=True, null=True , default="")
   

class GuestUsers(models.Model):
    device_id=models.CharField(max_length=200,primary_key=True)
    

