from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .mixins import ActiveCategoryListFilter, MainCategoryListFilter , ActiveCategoryListFilter
from . import models
# Register your models here.
class filterAdmin(admin.ModelAdmin):
    model = models.Filter
    search_fields = ('title',)
    list_filter = ('productcaegories' ,'packcategories' )
    #ordering = ('-title',)
    list_display = ('title', 'active')


class PackCategoryAdmin(admin.ModelAdmin):
    model = models.PackCategory
    search_fields = ('title' ,'description')
    list_filter = [MainCategoryListFilter , ActiveCategoryListFilter , 'parent']
    list_display = ('title' ,'is_main' ,'is_active' ,'created' )
    #ordering = ('-title',)
    fieldsets = (
        (None, {'fields': ('title', 'parent', 'description','is_active')}),
       
    )
    ordering = ('is_main','title' ,'is_active','created')

class ProductCategoryAdmin(admin.ModelAdmin):
    model = models.ProductCategory
    search_fields = ('title' ,'description')
    list_filter = [MainCategoryListFilter , ActiveCategoryListFilter]
    list_display = ('title' ,'is_main' ,'is_active' ,'created' )
    #ordering = ('-title',)
    fieldsets = (
        (None, {'fields': ('title', 'parent', 'description','is_active')}),
       
    )
    ordering = ('is_main','title' ,'is_active','created')

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = models.ProductCategory
    search_fields = ('title' ,'description')
    list_filter = [ActiveCategoryListFilter]
    list_display = ('title' ,'is_active' ,'created' )
    #ordering = ('-title',)
    fieldsets = (
        (None, {'fields': ('title', 'description','is_active')}),
       
    )
    ordering = ('title' ,'is_active','created')


class PackCategoryItemAdmin(admin.ModelAdmin):
    model = models.PackCategoryItem
    list_filter = ['packcategory__title',]
   
    list_display = ('id','Pack','Category','filters')

    @mark_safe
    def Pack(self, item):
        url = reverse('admin:products_pack_change', args=(item.pack.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.pack.title
        )
    Pack.short_description = "Article"
    @mark_safe
    def Category(self, item):
        url = reverse('admin:categories_packcategory_change', args=(item.packcategory.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.packcategory.title
        )
    Category.short_description = "Category"

    @mark_safe
    def filters(self, item):
        a=''
        list_filters =[]
        filters=item.filter.all()
        for element in filters :
            
            a=a +'<li style="display: inline; padding-left: 5px">' + element.title + '</li>'
       

        print(a)
        return '<ul style="list-style: none; padding-left: 0;"; href="#">{f}</ul>'.format(
            f=a
            
        )
    filters.short_description = "filters"



class ProductategoryItemAdmin(admin.ModelAdmin):
    model = models.ProductCategoryItem
    list_filter = ['productcategory__title',]
   
    list_display = ('id','Product','Category','filters')

    @mark_safe
    def Product(self, item):
        url = reverse('admin:products_product_change', args=(item.product.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.product.title
        )
    Product.short_description = "Article"
    @mark_safe
    def Category(self, item):
        url = reverse('admin:categories_productcategory_change', args=(item.productcategory.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.productcategory.title
        )
    Category.short_description = "Category"

    @mark_safe
    def filters(self, item):
        a=''
        list_filters =[]
        filters=item.filter.all()
        for element in filters :
            
            a=a +'<li style="display: inline; padding-left: 5px">' + element.title + '</li>'
       

        print(a)
        return '<ul style="list-style: none; padding-left: 0;"; href="#">{f}</ul>'.format(
            f=a
            
        )
    filters.short_description = "filters"
    
class ArticleCategoryItemAdmin(admin.ModelAdmin):
    model = models.ArticleCategoryItem
    list_filter = ['articlecategory__title',]
   
    list_display = ('id','Article','Category','filters')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article','articlecategory', 'filter')}
         ),
    )
    @mark_safe
    def Article(self, item):
        url = reverse('admin:products_article_change', args=(item.article.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.article.title
        )
    Article.short_description = "Article"
    @mark_safe
    def Category(self, item):
        url = reverse('admin:categories_articlecategory_change', args=(item.articlecategory.id, ))
        return '<a href="{url}">{user}</a>'.format(
             url=url, 
             user=item.articlecategory.title
        )
    Category.short_description = "Category"

    @mark_safe
    def filters(self, item):
        a=''
        list_filters =[]
        filters=item.filter.all()
        for element in filters :
            
            a=a +'<li style="display: inline; padding-left: 5px">' + element.title + '</li>'
       

        print(a)
        return '<ul style="list-style: none; padding-left: 0;"; href="#">{f}</ul>'.format(
            f=a
            
        )
    filters.short_description = "filters"


admin.site.register(models.ProductCategory ,ProductCategoryAdmin)
admin.site.register(models.PackCategory ,PackCategoryAdmin)
admin.site.register(models.ArticleCategory ,ArticleCategoryAdmin)
admin.site.register(models.Filter,filterAdmin)
admin.site.register(models.PackCategoryItem ,PackCategoryItemAdmin )
admin.site.register(models.ProductCategoryItem ,ProductategoryItemAdmin)
admin.site.register(models.ArticleCategoryItem ,ArticleCategoryItemAdmin)
