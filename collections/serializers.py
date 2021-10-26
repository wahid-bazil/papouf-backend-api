
from categories.models import Filter
from django.db import models
from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import get_object_or_404
from .models import Article ,Pack, Product
from rest_framework import serializers
#from category.models import ArticleCategory
#from media.serializers import ProductImageSerializer,BoxeImageSerializer




class ArticleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id','title','sale_price','description','type' ,'space','child' ,'variant_description']
    def get_type(self, obj):
        return obj._meta.verbose_name

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['images']



class ProductSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','title','sale_price','promo_price','description','type','status','promo' ,'promo_percentage']
    def get_type(self, obj):
        return obj._meta.verbose_name 



class PackSerializer(serializers.ModelSerializer):
    items =  ArticleSerializer(many=True,required=True)
    type = serializers.SerializerMethodField()
  
    class Meta:
        model = Pack
        fields = ['id','title','sale_price','items','is_customized','description','type' ]
    def get_type(self, obj):
        return obj._meta.verbose_name
 
            


    
    

