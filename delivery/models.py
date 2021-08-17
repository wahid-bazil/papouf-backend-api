from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django_countries.fields import CountryField



class Delivery_Mode(models.Model):
    title = models.CharField(max_length=30,primary_key=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
    description = models.CharField(max_length=300)


class ShippingRegion(models.Model):
    title = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.title
class ShippingCity(models.Model):
    #Country  = CountryField()
    region = models.ForeignKey(ShippingRegion,on_delete=models.CASCADE,blank=True,null=True ,related_name='cities')
    title = models.CharField(max_length=30 ,unique=True)
    def __str__(self):
        return self.title
    
class IntervalOrderToltal(models.Model):
    shipping_mode = ForeignKey('ShippingMode',on_delete=models.CASCADE ,null=True)
    min_total = models.FloatField()
    max_total = models.FloatField()


class ShippingHandler(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.title + '__id_' + str(self.id)

class ShippingMode(models.Model):
    free_shipping_min_total = models.FloatField()
    free_shipping_max_total = models.FloatField()
    title = models.CharField(max_length=30 ,unique=True)
    shipping_handler = models.ForeignKey(ShippingHandler,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title) + '/' + str(self.shipping_handler)



class ShippingItemType(models.Model):
    title= models.CharField(max_length=30)
    shipping_mode = models.ForeignKey('ShippingMode' ,on_delete=models.CASCADE)
    max_weight = models.FloatField()
    max_width = models.FloatField()
    max_height = models.FloatField()
    min_weight = models.FloatField()
    ma_width = models.FloatField()
    max_height = models.FloatField()
    additional_rate = models.PositiveIntegerField()
    def __str__(self):
        return str(self.title) + 'for' + str(self.shipping_mode)

class ShippingNetPrice(models.Model):
    total_order_interval = models.ForeignKey(IntervalOrderToltal , on_delete=models.CASCADE , null=True , blank=True)
    cities = models.ManyToManyField('ShippingCity')
    net_shipping_price =models.FloatField()
    shipping_mode = models.ForeignKey('ShippingMode' ,on_delete=models.CASCADE , null=True , blank=True)
    def __str__(self):
        return str(self.cities) + '__' + str(self.shipping_mode)

        
class ShippingDelay(models.Model):
    cities = models.ManyToManyField(ShippingCity)
    delay_per_hour = models.PositiveIntegerField()
    shipping_mode =models.ForeignKey(ShippingMode , on_delete=models.CASCADE , null=True , blank=True)








