from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from customization.models import CustomPack,CustomPackArticle,CustomPackUserImage
from rest_framework import serializers
from products.serializers import ArticleSerializer,BoxeSerializer
from users.serializers import UserMiniSerializer
from products.models import Boxe

class CustomPackArticleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    item=ArticleSerializer()
    class Meta :
        model = CustomPackArticle
        fields = ['id','item','quantity','total' ,'type']
    def get_type(self, obj):
        return obj._meta.verbose_name    


class CustomPackSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    packitems = CustomPackArticleSerializer(source='custompackarticle_set',many=True,required=True)
    boxe = BoxeSerializer()
    user = UserMiniSerializer()
    userimages_nb = serializers.SerializerMethodField()
    class Meta :
        model = CustomPack
        fields = ['id','title','sale_price','packitems','userimages_nb','boxe','type','user' ,'isCopy']
    def get_type(self, obj):
        return obj._meta.verbose_name
    def get_userimages_nb (self , obj):
        return len(obj.user_images.all())

class CustomPackUpdateBoxeSerializer(serializers.ModelSerializer):
    class Meta:
        Model = CustomPack
        fields = ['Boxe']

class CustomPackBoxeImageSerializer(serializers.ModelSerializer):
    #boxe = BoxeImageSerializer()
    class Meta:
        model =  CustomPack
        fields = ['boxe']