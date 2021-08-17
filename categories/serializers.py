from django.db.models import fields
from products.models import Pack
from django.contrib.auth import models
from rest_framework import serializers
from products.serializers import PackSerializer, ProductSerializer, ArticleSerializer
from .models import ArticleCategory, PackCategoryFilter, ProductCategory, PackCategory, ProductCategoryFilter
from media.serializers import ImagesProductSerializer

"""Product"""
class ProductCategoryFilterMiniSerializer(serializers.ModelSerializer):
    class Meta : 
        model = ProductCategoryFilter
        fields = ['title']

class ProductCategoryFilterSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True)
    class Meta:
        model = ProductCategoryFilter
        fields = ['title','category','items']


class ProductCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = ProductCategory
        fields = ['id','title', 'items', 'description']
    def get_items(self, obj):
        all_child = obj.get_children()
        items = []
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        return ProductSerializer(items,many=True).data

class ProductCategoryFilterListSerializer(serializers.ModelSerializer):
    filters = ProductCategoryFilterMiniSerializer(many=True)
    class Meta:
        model = ProductCategory
        fields = ['filters','title']


"""Pack"""

class PackCategoryFilterMiniSerializer(serializers.ModelSerializer):
    class Meta : 
        model = PackCategoryFilter
        fields = ['title']

class PackCategoryFilterSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True)
    class Meta:
        model = PackCategoryFilter
        fields = ['title','category','items']


class PackCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = PackCategory
        fields = ['id','title', 'items', 'description']
    def get_items(self, obj):
        print('here')
        all_child = obj.get_children()
        items = []
        items.extend(obj.items.all())
        
        for child in all_child:
            print(child)
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        return PackSerializer(items,many=True).data

class PackCategoryFilterListSerializer(serializers.ModelSerializer):
    filters = PackCategoryFilterMiniSerializer(many=True)
    class Meta:
        model = PackCategory
        fields = ['filters','title']










































class ImagesProductCategorySerializer(serializers.ModelSerializer):
    items = ImagesProductSerializer(many=True)
    class Meta:
        model = ProductCategory
        fields = ['items']




class ArticleCategorySerializer(serializers.ModelSerializer):
    items = ArticleSerializer(many=True)

    class Meta:
        model = ArticleCategory
        fields = ['title', 'items']


class ProductCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['title', 'description']


class PackCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackCategory
        fields = ['title', 'description']


class ArticleCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['title', 'description', 'img']


""" category test"""
