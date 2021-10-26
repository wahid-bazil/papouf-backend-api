from django.contrib import admin
from django.db import models
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'name','phone_number')
    list_filter = ('email', 'name','phone_number','is_email_verified' ,'verification_overridden', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'name','phone_number','is_email_verified','verification_overridden',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'name','phone_number' )}),
        ('Permissions', {'fields': ('groups','is_email_verified' ,'verification_overridden','is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('groups','email', 'name','phone_number', 'password1', 'password2','verification_overridden','is_email_verified' , 'is_active', 'is_staff')}
         ),
    )
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('Permissions')

        return super().get_form(request, obj, **kwargs)

class AdressAdminConfig(admin.ModelAdmin):
    model = Address
    list_display = ('user', 'city','details')






admin.site.register(NewUser ,UserAdminConfig)
admin.site.register(Address ,AdressAdminConfig)
admin.site.register(GuestUsers)
admin.site.register(RegistrationConfig)
