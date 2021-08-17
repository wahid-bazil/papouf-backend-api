
from django.db import models
from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import get_object_or_404
from products.models import Article, Boxe, Pack, Product, test
from rest_framework import serializers
#from category.models import ArticleCategory
#from media.serializers import ProductImageSerializer,BoxeImageSerializer





class BoxeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Boxe
        fields = ['id','title','sale_price' ,'description','space','type']
    def get_type(self, obj):
        return obj._meta.verbose_name

class ArticleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id','title','sale_price','description','type' ,'space','child' ,'variant_description']
    def get_type(self, obj):
        return obj._meta.verbose_name

class ArticleImageSerializer(serializers.ModelSerializer):
    #images=BoxeImageSerializer(many=True)
    class Meta:
        model = Article
        fields = ['images']



class ProductSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    #images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','title','sale_price','promo_price','description','type','status','promo' ,'promo_percentage']
    def get_type(self, obj):
        return obj._meta.verbose_name 



class PackSerializer(serializers.ModelSerializer):
    items =  ArticleSerializer(many=True,required=True)
    type = serializers.SerializerMethodField()
    boxe = BoxeSerializer()
    class Meta:
        model = Pack
        fields = ['id','title','sale_price','items','is_customized','boxe','description','type']
    def get_type(self, obj):
        return obj._meta.verbose_name


class testSerializer(serializers.ModelSerializer):
    #boxe= BoxeSerializer(read_only=True)
    class Meta:
        model  = test
        fields = '__all__'
        extra_kwargs = {"boxe": {"required": False, "allow_null": True}}    

    
    

class testArticleSerializer(serializers.ModelSerializer):
    class Meta :
        model  = Article
        fields = '__all__'

