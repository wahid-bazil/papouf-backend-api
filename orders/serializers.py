from users.serializers import AddressSerializer
from orders.models import Order 
from django.contrib.contenttypes import models
from rest_framework import fields, serializers
from cart.serializers import CartSerializer
from delivery.serializers import ShippingModeSerializer


""""class UserCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheckout
        fields = '__all__'"""


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    delivery_mode = ShippingModeSerializer()
    shipping_address =AddressSerializer()
    class Meta:
        model = Order
        fields = ['id','status','shipping_address','created','cart','delivery_mode' ,'shipping_address' ,'shipping_total_price' , 'order_total' ,'is_paid' , 'payment_mode','delay' ,'cost']

