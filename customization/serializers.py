from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from customization.models import CustomPack,CustomPackArticle,CustomPackUserImage
from rest_framework import serializers
from products.serializers import ArticleSerializer,BoxeSerializer
from users.serializers import UserMiniSerializer
from products.models import Boxe



class CreateCustomPackSerializer(serializers.ModelSerializer):
    pack_id = serializers.IntegerField(required=True)
    class Meta :
        model = CustomPack
        fields = ['pack_id']

class CreateCustomPackArticleSerializer(serializers.ModelSerializer):
    custompack_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    class Meta : 
        model = CustomPack
        fields = ['custompack_id' , 'item_id']
    

class CustomPackArticleSerializer(serializers.ModelSerializer):
    item_category = serializers.SerializerMethodField()
    item=ArticleSerializer()
    class Meta :
        model = CustomPackArticle
        fields = ['id','item','quantity','total','item_category']
    def get_item_category(self, obj):
        return obj.item.articlecategoryitem.articlecategory.title


class CustomPackSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    packitems = CustomPackArticleSerializer(source='custompackarticle_set',many=True,required=True)
    #user = UserMiniSerializer()
    userimages_nb = serializers.SerializerMethodField()
    class Meta :
        model = CustomPack
        fields = ['id','title','sale_price','packitems','userimages_nb','isCopy' ,'type']
    """def get_type(self, obj):
        return obj._meta.verbose_name"""
    def get_userimages_nb (self , obj):
        return len(obj.user_images.all())
    
    def get_type(self, obj):
        return obj._meta.verbose_name

class CustomPackUpdateBoxeSerializer(serializers.ModelSerializer):
    class Meta:
        Model = CustomPack
        fields = ['Boxe']

class CustomPackBoxeImageSerializer(serializers.ModelSerializer):
    #boxe = BoxeImageSerializer()
    class Meta:
        model =  CustomPack
        fields = ['boxe']

class PackCopySerializer(serializers.ModelSerializer):
    original_pack_id  = serializers.IntegerField()
    class Meta:
        model = CustomPack
        fields = ['original_pack_id']


class CustomPackArticleUpdate(serializers.ModelSerializer):
    article_id =serializers.IntegerField(required=False)
    class Meta : 
        model = CustomPackArticle
        fields = ['quantity' , 'article_id']


        