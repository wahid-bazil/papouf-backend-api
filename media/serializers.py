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


class ImageBoxeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxeImage
        fields = ['image']


class ImagesBoxeSerializer(serializers.ModelSerializer):
    images = ImageBoxeSerializer(many=True)
    boxe_id = serializers.SerializerMethodField()

    class Meta:
        model = Boxe
        fields = ['boxe_id', 'images']

    def get_boxe_id(self, obj):
        return obj.id


class ImageArticleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ArticleImage
        fields = ['image']

    def get_image(self, articleimage):
        request = self.context.get('request')
        print("r", request)
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
    image = serializers.SerializerMethodField()

    class Meta:
        model = CustomPackImage
        fields = ["image"]


""" """


class UserImagesCustomPackSerializer(serializers.ModelSerializer):
    images = UserImageCustomPackSerializer(many=True, source='user_images')

    class Meta:
        model = CustomPack
        fields = ['images']


class ImagesCustomPackSerializer(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = CustomPack
        fields = ['item_id', 'item_type', 'images']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name
    def get_images(self, obj):
        request = self.context.get('request')
        boxe_images = obj.boxe.images
        return ImageBoxeSerializer(boxe_images ,many=True ,context={"request": request}).data


class ImagesProductSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True)
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['images', 'item_id', 'item_type']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name


class ImagesPackSerializer(serializers.ModelSerializer):
    images = ImagePackSerializer(many=True)
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = Pack
        fields = ['images', 'item_id', 'item_type']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name


class ImagesArticleSerializer(serializers.ModelSerializer):
    images = ImageArticleSerializer(many=True)
    item_id = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['images', 'item_id', 'item_type']

    def get_item_id(self, obj):
        return obj.id

    def get_item_type(self, obj):
        return obj._meta.verbose_name



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
        CustomPack: ImagesCustomPackSerializer(),
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


class ImagesCustomPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPackImage
        fields = ['image', 'item']


class ImagesCustomPackArticleSerializer(serializers.ModelSerializer):
    custompackitem_images = ImagesArticleSerializer(source="item")
    custompackitem_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomPackArticle
        fields = ["custompackitem_images", "custompackitem_id"]

    def get_custompackitem_id(self, obj):
        return obj.id


class ImagesCustomPacArticlesSerializer(serializers.ModelSerializer):
    custompackitems_images = ImagesCustomPackArticleSerializer(
        many=True,  source="custompackarticle_set")
    custompack_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomPack
        fields = ["custompackitems_images", "custompack_id"]

    def get_custompack_id(self, obj):
        return obj.id


class ImagesCustomPackUserImageSeriazer(serializers.ModelSerializer):
    image_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomPackUserImage
        fields = ['image_id', 'image', 'quantity', 'total']

    def get_image_id(self, obj):
        return obj.id


class ImagesCustomPackUserImagesSeriazer(serializers.ModelSerializer):
    userimages = ImagesCustomPackUserImageSeriazer(
        source="user_images", many=True)

    class Meta:
        model = CustomPack
        fields = ['userimages']


class CustomPackImageSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomPackUserImage
        fields = '__all__'


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


class ImagesProductFilterSerializer(serializers.ModelSerializer):
    items = ImagesProductSerializer(many=True)

    class Meta:
        model = ProductCategoryFilter
        fields = ['items']

# PackCategory


class ImagesPackCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = PackCategory
        fields = ['items']
    def get_items(self, obj):
        all_child = obj.get__all_children()
        items = []
        print('here')
        items.extend(obj.items.all())
        for child in all_child:
            child_itmes = child.items.all()
            for item in child_itmes:
                if item not in items:
                    items.append(item)
        request = self.context.get('request')
        return ImagesPackSerializer(items, many=True, context={"request": request}).data


class ImagesPackFilterSerializer(serializers.ModelSerializer):
    items = ImagesPackSerializer(many=True)

    class Meta:
        model = PackCategoryFilter
        fields = ['items']


# Order


class ImagesOrderSerializer(serializers.ModelSerializer):
    cart_images = ImagesCartSerializer(source='cart')

    class Meta:
        model = Order
        fields = ['cart_images']
