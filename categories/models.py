
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField

"""
class PackType(models.Model):
    title = models.CharField(max_length=120, unique=True, primary_key=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    img = models.CharField(max_length=30, default="")
"""

class ProductCategory(models.Model):
    title = models.CharField(max_length=120, unique=True)
    parent = models.ForeignKey(
        'ProductCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    img = models.CharField(max_length=30, default="")
    items = models.ManyToManyField("products.Product", blank=True)

    def get_children(self):
        all_children = []
        # print(self.child.all())
        for first_child in self.child.all():
            all_children.append(first_child)
            all_children.extend(first_child.get_children())
        return all_children

    def __str__(self):
        return self.title

class ProductCategoryFilter(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='filters', null=True)
    title = models.CharField(max_length=15, null=False, unique=True)
    items = models.ManyToManyField("products.Product", blank=True)


class PackCategory(models.Model):
    title = models.CharField(max_length=120, unique=True)
    parent = models.ForeignKey(
        'PackCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    img = models.CharField(max_length=30, default="")
    items = models.ManyToManyField("products.Pack", blank=True  )

    def get_children(self):
        all_children = []
        # print(self.child.all())
        for first_child in self.child.all():
            all_children.append(first_child)
            all_children.extend(first_child.get_children())
        return all_children

    def __str__(self):
        return self.title

class PackCategoryFilter(models.Model):
    category = models.ForeignKey(
        PackCategory, on_delete=models.CASCADE, related_name='filters', null=True)
    title = models.CharField(max_length=15, null=False, unique=True)
    items = models.ManyToManyField("products.Pack", blank=True )






class ArticleCategory(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    img = models.CharField(max_length=30, default="")
    #pack_type = models.ForeignKey(
        #PackType, on_delete=CASCADE, blank=True, null=True)
