from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify, title


class ShippingBoxGroupe(models.Model):
    title =models.CharField(max_length=30)
    max_volume=models.FloatField()


class ShippingBox(models.Model):
    title= models.CharField(max_length=30)
    max_width = models.FloatField()
    max_length = models.FloatField()
    max_heigth = models.FloatField()


    

class Delivery_Mode(models.Model):
    title = models.CharField(max_length=30,primary_key=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
    description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100 , blank=True)
    def slug(self):
        return slugify(self.title)


class ShippingRegion(models.Model):
    title = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.title
    slug = models.CharField(blank=True , max_length=30)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ShippingRegion, self).save(
            force_insert, force_update, *args, **kwargs)

class ShippingCity(models.Model):
    region = models.ForeignKey(ShippingRegion,on_delete=models.CASCADE,blank=True,null=True ,related_name='cities')
    title = models.CharField(max_length=30 ,unique=True)
    slug = models.CharField(blank=True , max_length=30)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ShippingCity, self).save(
            force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.title

    
class IntervalOrderToltal(models.Model):
    shipping_mode = ForeignKey('ShippingMode',on_delete=models.CASCADE ,null=True)
    min_total = models.FloatField()
    max_total = models.FloatField()



class ShippingMode(models.Model):
    free_shipping_min_total = models.FloatField()
    free_shipping_max_total = models.FloatField()
    title = models.CharField(max_length=30 ,unique=True)
    slug = models.CharField(blank=True , max_length=30)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ShippingMode, self).save(
            force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title





class ShippingNetPrice(models.Model):
    total_order_interval = models.ForeignKey(IntervalOrderToltal , on_delete=models.CASCADE , null=True , blank=True)
    cities = models.ManyToManyField('ShippingCity')
    net_shipping_price =models.FloatField( verbose_name='cost')
    shipping_mode = models.ForeignKey('ShippingMode' ,on_delete=models.CASCADE , null=True , blank=True)
    def __str__(self):
        return str(self.cities) + '__' + str(self.shipping_mode)

        
class ShippingDelay(models.Model):
    cities = models.ManyToManyField(ShippingCity)
    delay_per_hour = models.PositiveIntegerField()
    shipping_mode =models.ForeignKey(ShippingMode , on_delete=models.CASCADE , null=True , blank=True)








