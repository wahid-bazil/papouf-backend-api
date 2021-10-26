from django.contrib import admin
from . import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class CustomPackAdmin(admin.ModelAdmin):
    model = models.CustomPack
    list_display = ('id','client' ,'device_id', 'created','cost_price','sale_price','isCopy','inCart')
    list_filter = ('user',)
    ordering = ('-created',)
    search_fields = ('title',)

    @mark_safe
    def client(self, item):
        if item.user  :
            url = reverse('admin:customization_custompack_change', args=(item.user.id, ))
            return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.user.email
            )
        else :
            return '-'
    client.short_description = "Client"



class CustomPackArticleAdmin(admin.ModelAdmin):
    model = models.Article
    #search_fields = ('email', 'name', 'second_name','phone_number')
    #list_filter = ('email', 'name', 'second_name','phone_number','is_email_verified' ,'verification_overridden', 'is_active', 'is_staff')
    #ordering = ('-start_date',)
    list_display = ('id','quantity','total')

admin.site.register(models.CustomPack ,CustomPackAdmin)
admin.site.register(models.CustomPackArticle ,CustomPackArticleAdmin)
admin.site.register(models.CustomPackSetting)
admin.site.register(models.CustomPackUserImage)


