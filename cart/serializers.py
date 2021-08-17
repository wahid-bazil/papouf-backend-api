

from products.models import Article
from cart.models import Cart, CartItem
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from products.serializers import * 
from django.contrib.contenttypes.models import ContentType
from customization.serializers import CustomPackSerializer,CustomPack





class CartItemSerializer(serializers.ModelSerializer):
    item = GenericRelatedField({
        Pack: PackSerializer(),
        Product: ProductSerializer(),
        Article : ArticleSerializer(),
        CustomPack:CustomPackSerializer()

    })
    class Meta:
            model = CartItem
            fields = ['id','quantity','item','total']


class CartItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
            model = CartItem
            fields = ['quantity']

class tests(serializers.ModelSerializer):

    class Meta :
            model = CartItem
            fields = '__all__'   


class CartSerializer(serializers.ModelSerializer):
    cartitems= CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ["subtotal","cartitems"]

"""class CartinfoSerializer(serializers.ModelSerializer):
    items = Cart.cartitem_set.all().count()
    class Meta:
        model = Cart
        fields =['subtotal','items']"""
