
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
from .serializers import OrderSerializer   # UserCheckoutSerializer
from cart.models import Cart
from delivery.models import *
from users.models import Address
from .mixins import MethodSerializerView
#from payment.models import *


class OrderList(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrderSerializer
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset 
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            cart = get_object_or_404(Cart ,user=self.request.user ,active=True)
            for cartitem in cart.cartitems.all():
                item_id=cartitem.object_id
                item_type=cartitem.content_type
                if item_type == 'product':
                    item = get_object_or_404(Product, pk=item_id)
                    if cartitem.quantity > item.inventory:
                        raise NotAcceptable('the quantity of' + item.title +'is more than our inventory')
                elif item_type == 'pack' :
                    item = get_object_or_404(Pack, pk=item_id)
                    if cartitem.quantity > item.inventory:
                        raise NotAcceptable('the quantity of' + item.title +'is more than our inventory')
                elif item_type == 'custompack' :
                    item = get_object_or_404(CustomPack, pk=item_id)
                    packarticles=item.custompackarticle_set.all()
                    for packarticle in packarticles:
                        if packarticle.item.inventory > packarticle.quantity:
                            raise NotAcceptable('the custom pack' + item.title + 'contains an article with a quantity more than our inventory')
            serializer.save()
            cart.active=False
            cart.save()
            Cart.objects.create(user=self.request.user)           
            
        

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