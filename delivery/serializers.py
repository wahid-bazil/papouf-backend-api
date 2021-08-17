from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *

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