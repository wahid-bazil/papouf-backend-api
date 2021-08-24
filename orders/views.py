
#from orders.models import UserCheckout

#from delivery.models import Delivery_Mode
from orders.models import Order
from typing import cast
from django.shortcuts import render
from django.views import generic
from customization.models import CustomPack
from django.contrib.auth.models import User
from django.http import request
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from products.models import Article, Pack, Product
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError, PermissionDenied
from users.models import Address, GuestUsers, NewUser
from rest_framework.views import APIView
from .serializers import OrderSerializer  # UserCheckoutSerializer
from cart.models import Cart
from delivery.models import *
from users.models import Address
#from payment.models import *
"""class UserCheckout(CreateAPIView):
    
    serializer_class=UserCheckoutSerializer
    def create(self, request, *args, **kwargs):
        
        serializer=UserCheckoutSerializer(user=self.request.user , email=self.request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)"""


class OrderList(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user=self.request.user
            address = get_object_or_404(Address , user=user )
            shipping_mode = str(request.data['shipping_mode'])
            total = str(request.data['total'])
            delay = int(request.data['delay'])
            cost = int(request.data['cost'])
            #payment_mode = str(request.data['payment_mode'])

        except:
            pass

        cart = Cart.objects.filter(user=self.request.user, active=True).first()
        delivery_mode = get_object_or_404(ShippingMode, title="Livraison Standart")
        payment_mode ="Paiement à la livraison"
        if payment_mode == "Paiement à la livraison":
            is_paid = False
        else:
            is_paid = True
        Order.objects.create(user=self.request.user,shipping_address=address, cart=cart,
                             delivery_mode=delivery_mode, payment_mode=payment_mode,is_paid=is_paid,order_total=total ,delay=delay ,cost=cost)
        return Response(status.HTTP_201_CREATED)

class OrderDetail(RetrieveAPIView):
    queryset= Order.objects.all()
    serializer_class = OrderSerializer


class OrdersLenght(ListAPIView):
    permission_classes =[IsAuthenticated]
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset
    def list(self, request, *args, **kwargs):
        orders=self.get_queryset()
        return Response (len(orders),status=status.HTTP_200_OK)
    