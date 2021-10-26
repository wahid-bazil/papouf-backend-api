from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe
from django.urls import reverse
# Register your models here.


class cartAdmin(admin.ModelAdmin):
    model = models.Cart
    search_fields = ('id', 'active', 'subtotal','device_id','timestamp')
    list_filter = ('user', 'active')
    ordering = ('-timestamp',)
    list_display = ('id','client','active', 'subtotal','timestamp','device_id',)

    @mark_safe
    def client(self, cart):
        if cart.user  :
            url = reverse('admin:users_newuser_change', args=(cart.user.id, ))
            return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=cart.user.email
            )
        else :
            return '-'
    client.short_description = "client"


  
admin.site.register(models.Cart,cartAdmin)
admin.site.register(models.CartItem)
