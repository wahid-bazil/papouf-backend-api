
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
from users.models import GuestUsers, NewUser
from rest_framework.views import APIView
from .serializers import OrderSerializer  # UserCheckoutSerializer
from cart.models import Cart


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
            delivery_mode = str(request.data['delivery_mode'])
            payment_mode = str(request.data['payment_mode'])

        except:
            pass

        cart = Cart.objects.filter(user=self.request.user, active=True).first()
        #delivery_mode = get_object_or_404(Delivery_Mode,  pk=delivery_mode)
        #payment_mode = get_object_or_404(Payment_Mode, pk=payment_mode)
        if payment_mode == "CashOnDelivery":
            is_paid = False
        else:
            is_paid = True
        Order.objects.create(user=self.request.user, cart=cart,
                             delivery_mode=delivery_mode, payment_mode=payment_mode)
        return Response(status.HTTP_201_CREATED)

class OrderDetail(RetrieveAPIView):
    queryset= Order.objects.all()
    serializer_class = OrderSerializer
