

from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *


class ShippingDelayCostSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=30 , required=True)
    order_total = serializers.FloatField()
    shipping_mode = serializers.CharField(max_length=30 , required=True)
    class Meta:
        model = ShippingMode
        fields= ['city' , 'order_total' , 'shipping_mode']


class ShippingCitySerializer(serializers.ModelSerializer):
    class Meta :
        model = ShippingCity
        fields =['title']

class ShippingRegionMiniSerializer(serializers.ModelSerializer):
    class Meta : 
        model = ShippingRegion
        fields =['title' ]

        
class ShippingRegionSerializer(serializers.ModelSerializer):
    cities = ShippingCitySerializer(many=True)
    class Meta : 
        model = ShippingRegion
        fields =['title' , 'cities']



class ShippingModeSerializer(serializers.ModelSerializer):
    class Meta :
        model = ShippingMode
        fields =['title']
