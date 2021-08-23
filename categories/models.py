
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from django.utils import tree


"""class PackType(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    img = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.title + '/' + 'id=' + str(self.id)
    def get_main_categories (self) :
        categories = self.categories.all()
        main_categories = []
        for category in categories:
            if category.parent==None:
                main_categories.append(category)
        return main_categories
"""
    
   
        



class ProductCategory(models.Model):
    label = models.CharField(max_length=50,unique=True , null=True)
    title = models.CharField(max_length=120, unique=True)
    parent = models.ForeignKey(
        'ProductCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    img = models.CharField(max_length=30, default="")
    items = models.ManyToManyField("products.Product", blank=True)
    #type = models.ForeignKey(PackType,on_delete=models.CharField, blank=True,null=True)

    def get_children(self):
        all_children = []
        # print(self.child.all())
        for first_child in self.children.all():
            all_children.append(first_child)
            all_children.extend(first_child.get_children())
        return all_children

    def __str__(self):
        return self.title + '/' + 'id=' + str(self.id)


class ProductCategoryFilter(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='filters', null=True)
    title = models.CharField(max_length=15, null=False, unique=True)
    items = models.ManyToManyField("products.Product", blank=True)

    def __str__(self):
        return self.title


class PackCategory(models.Model):
    title = models.CharField(max_length=120, unique=True )
    label = models.CharField(max_length=50,unique=True ,null=True)
    parent = models.ForeignKey(
        'PackCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    img = models.CharField(max_length=30, default="")
    items = models.ManyToManyField("products.Pack", blank=True)
    article_categories = models.ManyToManyField("ArticleCategory",null=True,blank=True)
    def __str__(self):
        return self.title + '/' + 'id=' + str(self.id)
    def get__all_children(self):
        all_children = []
        # print(self.child.all())
        for first_child in self.children.all():
            all_children.append(first_child)
            all_children.extend(first_child.get__all_children())
        return all_children



class PackCategoryFilter(models.Model):
    category = models.ForeignKey(
        PackCategory, on_delete=models.CASCADE, related_name='filters', null=True)
    title = models.CharField(max_length=15, null=False, unique=True)
    items = models.ManyToManyField("products.Pack", blank=True)


class ArticleCategory(models.Model):
    title = models.CharField(max_length=120, unique=True)
    label = models.CharField(max_length=50,unique=True ,null=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    img = models.CharField(max_length=30, default="")
    items = models.ManyToManyField("products.Article", blank=True ,null=True)

