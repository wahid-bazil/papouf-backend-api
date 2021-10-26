from django.db import models
from collections.models import Product
from collections.models import Article


class Provider (models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone_number =models.CharField(max_length=30)
    description=models.CharField(max_length=30)
    products= models.ManyToManyField(Product)
    articles= models.ManyToManyField(Article)
    
