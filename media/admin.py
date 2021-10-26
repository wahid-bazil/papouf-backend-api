from django.contrib import admin
from . import models

class PackImageAdmin(admin.ModelAdmin):
    model = models.PackImage
   
    list_display = ('id','item', 'main_image')


class ArticleImageAdmin(admin.ModelAdmin):
    model = models.ArticleImage
   
    list_display = ('id','item')


class ProductImageAdmin(admin.ModelAdmin):
    model = models.ProductImage
   
    list_display = ('id','item')


admin.site.register(models.CustomPackImage)

admin.site.register(models.ArticleImage)

