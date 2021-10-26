

from collections.models import Article
from cart.models import Cart, CartItem
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from collections.serializers import * 
from django.contrib.contenttypes.models import ContentType
from customization.serializers import CustomPackSerializer,CustomPack





class CartItemSerializer(serializers.ModelSerializer):
    cartitem_id =serializers.SerializerMethodField()
    item = GenericRelatedField({
        Pack: PackSerializer(),
        Product: ProductSerializer(),
        Article : ArticleSerializer(),
        CustomPack:CustomPackSerializer()

    },)
   
    class Meta:
            model = CartItem
            fields = ['cartitem_id','quantity','item','total']
          
    def get_cartitem_id(self,obj):
        return obj.id

class CreateCartItemSerializer(serializers.ModelSerializer):
    item_id=serializers.IntegerField(required=True,write_only=True)
    item_type=serializers.CharField(max_length=10, write_only=True)
    class Meta : 
        model = CartItem
        fields=['item_id','item_type']
    


class UpdateCartItemSerializer(serializers.ModelSerializer):
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


