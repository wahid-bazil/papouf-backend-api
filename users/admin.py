from django.contrib import admin
from django.db import models
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'name', 'second_name','phone_number')
    list_filter = ('email', 'name', 'second_name','phone_number', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'name', 'second_name','phone_number',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'second_name','phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'second_name','phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )



admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Address)
admin.site.register(GuestUsers)
