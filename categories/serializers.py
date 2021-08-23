from django.db.models import fields
from django.db.models.base import Model
from products.models import Pack
from django.contrib.auth import models
from rest_framework import serializers
from products.serializers import PackSerializer, ProductSerializer, ArticleSerializer
from .models import ArticleCategory, PackCategoryFilter, ProductCategory, PackCategory, ProductCategoryFilter
from media.serializers import ImagesProductSerializer


###########################ArticleCategory###############################
class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = ArticleCategory
        fields = ['title' , 'label' , 'description' ,'img']

class ArticleCategoryItemsSerializer(serializers.ModelSerializer):
    items = ArticleSerializer(many=True)
    class Meta :
        model = ArticleCategory
        fields =['title' , 'label' , 'description', 'items']
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

class ProductCategoryChildrenSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    class Meta :
        model =ProductCategory
        fields = ['id','title','label','children']
    def get_children(self,obj):
        return ProductCategoryChildrenSerializer(obj.children , many=True).data

class ProductCategoryFilterListSerializer(serializers.ModelSerializer):
    filters = ProductCategoryFilterMiniSerializer(many=True)
    class Meta:
        model = ProductCategory
        fields = ['filters','title']

############################################# Packs #########################################

                        ################# PackCategory ##################
class PackCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = PackCategory
        fields = ['id','title','label', 'items', 'description']
    def get_items(self, obj):
        all_child = obj.get__all_children()
        items = []
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        return PackSerializer(items,many=True).data
class PackCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackCategory
        fields = ['id','title' ,'label']


class PackCategoryChildrenSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    class Meta:
        model = PackCategory
        fields = ['id','title','label','children']
    def get_children(self,obj):
        return PackCategoryChildrenSerializer(obj.children , many=True).data

class PackArticleCategorySerializer(serializers.ModelSerializer):
    article_categories = ArticleCategorySerializer(many=True)
    class Meta :
        model = PackCategory
        fields = ['article_categories']
                        ######################### PackType ####################
"""
class PackTypeSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta :
        model = PackType
        fields = ['title','categories']
    def get_categories(self,obj):
        categories = obj.get_main_categories()
        return PackCategoryChildrenSerializer(categories,many=True).data
"""

                        ######################### PackFilter ####################

class PackCategoryFilterMiniSerializer(serializers.ModelSerializer):
    class Meta : 
        model = PackCategoryFilter
        fields = ['title']

class PackCategoryFilterSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True)
    class Meta:
        model = PackCategoryFilter
        fields = ['title','category','items']

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




"""class ArticleCategorySerializer(serializers.ModelSerializer):
    items = ArticleSerializer(many=True)

    class Meta:
        model = ArticleCategory
        fields = ['title', 'items']
"""
class ProductCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['title', 'description']


class PackCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackCategory
        fields = ['title', 'description']

"""
class ArticleCategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['title', 'description', 'img']
"""

""" category test"""
