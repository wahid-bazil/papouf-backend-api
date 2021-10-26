from warnings import filters
from django.db.models import fields
from django.db.models.base import Model
from products.models import Pack
from django.contrib.auth import models
from rest_framework import serializers
from products.serializers import PackSerializer, ProductSerializer, ArticleSerializer
from .models import ArticleCategory, Filter, PackCategoryItem, ProductCategory, PackCategory, ProductCategoryItem


#filter 
class filterMiniSerializer(serializers.ModelSerializer):
    class Meta :
        model = Filter
        fields =['title' ,'slug' ,'description']


#Article
class ArticleCategoryMiniSerializer(serializers.ModelSerializer):
    images =serializers.SerializerMethodField()
    class Meta :
        model = ArticleCategory
        fields =['title'  , 'description' ,'images' ,'slug']
    def get_images(self, obj):
        images =[]
        request = self.context.get('request')
        images_queryset = obj.images.all()
        for element in images_queryset :
            image = element.image.url
            images.append(request.build_absolute_uri(image))
        return images

class ArticleCategorySerializer(serializers.ModelSerializer):
    items = ArticleSerializer(many=True)
    class Meta :
        model = ArticleCategory
        fields =['title'  , 'description', 'slug' ,'items']

class ArticleCategoriesTreeSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = ProductCategory
        fields = ['id','title', 'items','slug' ,'description']
    def get_items(self, obj):
        all_child = obj.get_children()
        items = []
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        return ArticleSerializer(items,many=True).data

#Products

class ProductCategoryMiniSerializer(serializers.ModelSerializer):
    filters = filterMiniSerializer(source='filter_set' ,many=True)
    class Meta :
        model = ProductCategory
        fields = ['id','title', 'description' ,'filters']

class ProductCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    filters = filterMiniSerializer(source='filter_set' ,many=True)
    class Meta:
        model = ProductCategory
        fields = ['id','title', 'items', 'description' ,'filters']
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

class ProductCategoriesTreeSerializer(serializers.ModelSerializer):   # Good one ! ^-^
    children=serializers.SerializerMethodField()
    class Meta :
        model =ProductCategory
        fields = ['id','title','children']
    def get_children(self,obj):
        return ProductCategoriesTreeSerializer(obj.children , many=True).data  






#Packs

class PackCategoryMiniSerializer(serializers.ModelSerializer):
    filters = filterMiniSerializer(source='filter_set' ,many=True)
    class Meta :
        model = ProductCategory
        fields = ['id','title', 'description' ,'filters']


class PackCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    filters = filterMiniSerializer(source='filter_set' ,many=True)
    class Meta:
        model = PackCategory
        fields = ['id','title', 'items', 'description' ,'filters' ]
    
    def get_items(self, obj):
        all_child = obj.get_children()
        items = []
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        if self.context.get("postsPerPage") and self.context.get("page"):
            postsPerPage = self.context.get("postsPerPage")
            page = self.context.get("page")
            start = postsPerPage * (page-1)
            return PackSerializer(items[start:start+postsPerPage],many=True).data
        else:
            return PackSerializer(items,many=True).data

class PackCategoriesTreeSerializer(serializers.ModelSerializer):   # Good one ! ^-^
    children=serializers.SerializerMethodField()
    class Meta :
        model =PackCategory
        fields = ['id','title','children']
    def get_children(self,obj):
        return PackCategoriesTreeSerializer(obj.children , many=True).data  




class PackArticlesCategoriesSerializer(serializers.ModelSerializer):
    articles_categories = ArticleCategorySerializer(many=True)
    class Meta : 
        model = PackCategory
        fields = ['articles_categories']

































































