from django.contrib import admin
from django.db.models import fields
from django.forms import ModelForm
from .models import *
from django.utils.html import format_html
# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe
from django.urls import reverse
class AbcStaffForm(ModelForm):
    class Meta:
        model = Order
        fields = ["status"]

class categoryAdmin(admin.ModelAdmin):
    model = Order
    search_fields = ('user', 'status', 'is_paid')
    list_filter = ('status', 'is_paid')
    ordering = ('-created',)
    readonly_fields = ('user_link', )
    list_display = ('id','status', 'user_link','order_total','created' ,'is_paid','shipping_total_price','payment_mode')
    
    @mark_safe
    def user_link(self, order):
        url = reverse('admin:users_newuser_change', args=(order.user.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=order.user
        )
    user_link.short_description = "Client"
    
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            kwargs['form'] = AbcStaffForm  # ModelForm

        return super().get_form(request, obj, **kwargs)


  


admin.site.register(Order,categoryAdmin)
admin.site.register(OrderEmail)