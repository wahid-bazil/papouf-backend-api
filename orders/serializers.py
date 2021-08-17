from orders.models import Order 
from django.contrib.contenttypes import models
from rest_framework import fields, serializers
from cart.serializers import CartSerializer


""""class UserCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheckout
        fields = '__all__'"""


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = ['id','status' ,'created','cart','delivery_mode' ,'shipping_address' ,'shipping_total_price' , 'order_total' ,'is_paid' , 'payment_mode']

