from django.contrib import admin
from . import models
# Register your models here.





class PackAdmin(admin.ModelAdmin):
    model = models.Pack
    #search_fields = ('email', 'name', 'second_name','phone_number')
    #list_filter = ('email', 'name', 'second_name','phone_number','is_email_verified' ,'verification_overridden', 'is_active', 'is_staff')
    #ordering = ('-start_date',)
    list_display = ('id','title', 'cost_price', 'sale_price','active','status','inventory','is_customized','orders')


class ProductAdmin(admin.ModelAdmin):
    model = models.Pack
    #search_fields = ('email', 'name', 'second_name','phone_number')
    #list_filter = ('email', 'name', 'second_name','phone_number','is_email_verified' ,'verification_overridden', 'is_active', 'is_staff')
    #ordering = ('-start_date',)
    list_display = ('id','title', 'cost_price', 'sale_price','active','status','inventory','orders')

class ArticleAdmin(admin.ModelAdmin):
    model = models.Article
    #search_fields = ('email', 'name', 'second_name','phone_number')
    #list_filter = ('email', 'name', 'second_name','phone_number','is_email_verified' ,'verification_overridden', 'is_active', 'is_staff')
    #ordering = ('-start_date',)
    list_display = ('id','title', 'cost_price', 'sale_price','active','inventory',)

class PackArticleAdmin(admin.ModelAdmin):
    model = models.PackArticle
    #search_fields = ('email', 'name', 'second_name','phone_number')
    list_filter = ('item','pack')
    #ordering = ('-start_date',)
    list_display = ('id','pack','item')

admin.site.register(models.Product ,ProductAdmin)

admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.PackArticle ,PackArticleAdmin)
admin.site.register(models.Pack ,PackAdmin)
admin.site.register(models.ProductFeature)
admin.site.register(models.ItemStatus)