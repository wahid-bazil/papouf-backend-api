from datetime import timezone

from rest_framework.exceptions import NotFound
from delivery.models import ShippingMode
from users.serializers import AddressSerializer
from orders.models import Order 
from django.contrib.contenttypes import models
from rest_framework import fields, serializers
from cart.serializers import CartSerializer
from delivery.serializers import ShippingModeSerializer
from django.utils.timezone import datetime
from payment.models import PaymentMode
from django.shortcuts import get_object_or_404
from cart.models import Cart
from users.models import Address
from delivery.models import *
""""class UserCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheckout
        fields = '__all__'"""


class OrderSerializer(serializers.ModelSerializer):
    shipping_mode = serializers.CharField(max_length=30 , required = True)
    payment_mode = serializers.CharField(max_length=30 , required = True)
    shipping_address =serializers.SerializerMethodField()
    remaining_time_hours = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display' ,required=False)
    class Meta : 
        model = Order
        fields = ['id','shipping_mode' , 'payment_mode' ,'shipping_address' ,'shipping_total_price','shipping_time','order_total','is_paid','payment_mode','remaining_time_hours' ,'created' ,'cart' ,'status']
        read_only_fields = ('shipping_address', 'shipping_total_price','shipping_time','order_total','is_paid','payment_mode' ,'created' ,'id','cart' ,'status')
    def get_remaining_time_hours(self,obj):
            created=obj.created
            shipping_time=obj.shipping_time
            elapsed_time=datetime.now(timezone.utc)-created
            elapsed_time_hours = elapsed_time.total_seconds()/3600
            remaining_time_hours = shipping_time -  elapsed_time_hours
            return int(remaining_time_hours)
    def get_shipping_address(self,obj):
        return AddressSerializer(obj.user.address_details).data
    def create(self, validated_data):
        shipping_mode = validated_data.pop('shipping_mode', None)
        payment_mode = validated_data.pop('payment_mode', None)
        print(shipping_mode ,'ll')
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            cart = get_object_or_404(Cart ,user=user, active=True)
            address = get_object_or_404(Address , user=user)
            city=address.city
            if city is None : 
                 raise NotFound(detail="you don't have an address ")
            try :
                shipping_mode=ShippingMode.objects.get(slug=shipping_mode)
            except : 
                raise NotFound(detail='this shipping mode does not exist ')
            try :
                payment_mode=PaymentMode.objects.get(slug=payment_mode)
            except : 
                raise NotFound(detail='this payment mode does not exist ')
            cart_subtotal=cart.subtotal
            shipping_time = ShippingDelay.objects.get(
                cities__in=[city], shipping_mode=shipping_mode).delay_per_hour
            total_order_interval = IntervalOrderToltal.objects.get(
                min_total__lte=cart_subtotal, max_total__gte=cart.subtotal, shipping_mode=shipping_mode)
            shipping_total_price = ShippingNetPrice.objects.get(
                shipping_mode=shipping_mode, total_order_interval=total_order_interval, cities__in=[city]).net_shipping_price
            order_total = cart_subtotal + shipping_total_price
            if payment_mode.title == "CashOnDelivery":
                is_paid = False
            else:
                is_paid = True
         
            instance=self.Meta.model(shipping_mode=shipping_mode,payment_mode=payment_mode ,user=user,shipping_address=address,cart=cart,is_paid=is_paid,order_total=order_total,shipping_time=shipping_time,shipping_total_price=shipping_total_price )
            instance.save()
            return instance
        
        












    

