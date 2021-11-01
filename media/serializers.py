#from Orders.models import Order
#from category.models import ArticleCategory
from django.db import models
from django.db.models.base import Model
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import RetrieveAPIView
from customization.models import CustomPack, CustomPackArticle, CustomPackUserImage
from django.db.models import fields
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from .models import ArticleImage, PackImage, ProductImage, BoxeImage, CustomPackImage
from cart.models import Cart, CartItem
from products.models import Article, Boxe, Pack, Product
from categories.models import *
from orders.models import *


class ImageProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image']
    def get_image(self, productimage):
        request = self.context.get('request')
        image = productimage.image.url
        return request.build_absolute_uri(image)


class ImagePackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackImage
        fields = ['image']









class ImageArticleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ArticleImage
        fields = ['image']

    def get_image(self, articleimage):
        request = self.context.get('request')
        image = articleimage.image.url
        return request.build_absolute_uri(image)


class imagePackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackImage
        fields = ['image']


class UserImageCustomPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPackUserImage
        fields = ['id', 'image', 'quantity', 'custompack', 'total']
        extra_kwargs = {"image": {"required": False}}


class ImageCustomPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPackImage
        fields = ["image"]


""" """


class UserImagesCustomPackSerializer(serializers.ModelSerializer):
    images = UserImageCustomPackSerializer(many=True, source='user_images')

    class Meta:
        model = CustomPack
        fields = ['images']


class ImagesMainCustomPackSerializer(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    images =serializers.SerializerMethodField()
    #ImageCustomPackSerializer(source="main_image" , many=True)
    class Meta:
        model = CustomPack
        fields = ['item_id', 'item_type', 'images']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name
    
    def get_images(self ,obj):
        images=[]
        request = self.context.get('request')
        imagesDict = ImageCustomPackSerializer(obj.main_image , many=True ,context={"request": request}).data
        for element in imagesDict:
            images.append(element['image'])

        return images


    """def get_images(self, obj):
        request = self.context.get('request')
        boxe_images = obj.boxe.images
     return ImageBoxeSerializer(boxe_images ,many=True ,context={"request": request}).data"""


class ImagesProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['images', 'item_id', 'item_type']
    def get_item_id(self, obj):
        return obj.id
    def get_item_type(self, obj):
        return obj._meta.verbose_name
    def get_images (self,obj):
        images=[]
        request = self.context.get('request')
        imagesDict = ImageProductSerializer(obj.images , many=True ,context={"request": request}).data
        for element in imagesDict:
            images.append(element['image'])

        return images
        


class ImagesPackSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    class Meta:
        model = Pack
        fields = ['images', 'item_id', 'item_type']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name
    def get_images (self,obj):
        images=[]
        imagesDict = ImagePackSerializer(obj.images , many=True).data
        for element in imagesDict:
            images.append(element['image'])
        return images
        


class ImagesArticleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    #images = ImageArticleSerializer(many=True)
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['images', 'item_id', 'item_type']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name
    
    def get_images(self, obj):
        images =[]
        request = self.context.get('request')
        images_queryset = obj.images.all()
        for element in images_queryset :
            image = element.image.url
            images.append(request.build_absolute_uri(image))
        return images
        
     


class ImagesArticleCategorySerializer(serializers.ModelSerializer):
    items = ImagesArticleSerializer(many=True)

    class Meta:
        model = ArticleCategory
        fields = ['items']


""" cart"""


class ImagesCartItemSerializer(serializers.ModelSerializer):
    cartitem_id = serializers.SerializerMethodField()
    cartitem_images = GenericRelatedField({
        Product: ImagesProductSerializer(),
        CustomPack: ImagesMainCustomPackSerializer(),
        Pack: ImagesPackSerializer()
    }, source="item")

    class Meta:
        model = CartItem
        fields = ['cartitem_images', 'cartitem_id']

    def get_cartitem_id(self, obj):
        return obj.id


class ImagesCartSerializer(serializers.ModelSerializer):
    cartitems_images = ImagesCartItemSerializer(many=True, source='cartitems')

    class Meta:
        model = Cart
        fields = ['cartitems_images']


"""custompack"""
class ImagesMainCustomPackSerializer(serializers.ModelSerializer):
    class Meta :
        model = CustomPackImage
        fields = ['image']

class ImagesCustomPackSerializer(serializers.ModelSerializer):
    packitems_images = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    class Meta :
        model = CustomPack
        fields = ['id' , 'title' ,'main_image', 'packitems_images' ]
    
    def get_main_image (self,obj) :
        request = self.context.get('request')
        return ImagesMainCustomPackSerializer(obj.main_image.all().first() ,context={"request": request}).data['image']
    def get_packitems_images (self ,obj) :
        packitems= CustomPackArticle.objects.filter(custompack=obj)
        articles = []
        for element in packitems:
            articles.append(element.item)
            request = self.context.get('request')
        return ImagesArticleSerializer(articles , many=True , context={"request": request} ).data





""" ProductCategory"""


class ImagesProductCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = ProductCategory
        fields = ['items']

    def get_items(self, obj):
        all_child = obj.get_children()
        items = []
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        request = self.context.get('request')
        return ImagesProductSerializer(items, many=True, context={"request": request}).data




# PackCategory


class ImagesPackCategorySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = PackCategory
        fields = ['images']
    def get_images(self, obj):
        all_child = obj.get_children()
        items = []
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        request = self.context.get('request')
        return ImagesPackSerializer(items, many=True, context={"request": request}).data



# Order


class ImagesOrderSerializer(serializers.ModelSerializer):
    cart_images = ImagesCartSerializer(source='cart')

    class Meta:
        model = Order
        fields = ['cart_images']
