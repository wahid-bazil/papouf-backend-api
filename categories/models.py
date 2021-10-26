
from collections.models import Article, Pack, Product
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey
from django.utils import tree
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class ProductCategory(models.Model):
    title = models.CharField(max_length=120 )
    is_main = models.BooleanField(
        default=False, verbose_name="Principal category", null=False, blank=False)
    parent = models.ForeignKey(
        'ProductCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    items = models.ManyToManyField(
        "products.Product", through='ProductCategoryItem')
    slug = models.CharField(blank=True , max_length=120)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.parent is None:
            self.is_main = True
        else:
            self.is_main = False
        super(ProductCategory, self).save(
            force_insert, force_update, *args, **kwargs)



    class Meta:
        verbose_name = '1.Product Categorie'


class PackCategory(models.Model):
    title = models.CharField(max_length=120)
    is_main = models.BooleanField(
        default=False, verbose_name="Principal category", null=False, blank=False)
    parent = models.ForeignKey(
        'PackCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='children' ,verbose_name="Child of ")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="active")
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    items = models.ManyToManyField("products.Pack", through='PackCategoryItem')
    articles_categories = models.ManyToManyField("ArticleCategory", blank=True)
    slug = models.CharField(blank=True , max_length=30)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.parent is None:
            self.is_main = True
        else:
            self.is_main = False
        super(PackCategory, self).save(
            force_insert, force_update, *args, **kwargs)
            
        
    class Meta:
        verbose_name = '2.Pack Categorie'


class ArticleCategory(models.Model):
    title = models.CharField(max_length=120, verbose_name="category")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="active")
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    slug = models.CharField(blank=True , max_length=30)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticleCategory, self).save(
            force_insert, force_update, *args, **kwargs)

   
    class Meta:
        verbose_name = '3.Article Categorie'
    def __str__(self) -> str:
        return self.title



class Filter(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    productcaegories = models.ManyToManyField(ProductCategory, blank=True)
    packcategories = models.ManyToManyField(PackCategory, blank=True)
    articlecategories = models.ManyToManyField(ArticleCategory, blank=True)
    slug = models.CharField(blank=True , max_length=30)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Filter, self).save(
            force_insert, force_update, *args, **kwargs)
    class Meta:
        verbose_name = '7.Category filter'


class PackCategoryItem(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    packcategory = models.ForeignKey(PackCategory, on_delete=models.CASCADE)
    filter = models.ManyToManyField(Filter ,blank=True)


    class Meta:
        verbose_name = '6.Pack categorie Item'


class ProductCategoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productcategory = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    filter = models.ManyToManyField(Filter, blank=True)

    class Meta:
        verbose_name = '5.Product categorie Item'


class ArticleCategoryItem(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE ,null=True , blank=True )
    articlecategory = models.ForeignKey(
        ArticleCategory, on_delete=models.CASCADE)
    filter = models.ManyToManyField(Filter, blank=True)

    class Meta:
        verbose_name = '6.Article categorie Item'
