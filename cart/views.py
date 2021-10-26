

from django.db.models import query
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
from .models import Cart, CartItem
from .serializers import CartItemSerializer, UpdateCartItemSerializer, tests,CartSerializer,CreateCartItemSerializer
from rest_framework.exceptions import NotAcceptable, NotAuthenticated, NotFound, ValidationError, PermissionDenied
from users.models import GuestUsers, NewUser
from rest_framework.views import APIView
from media.serializers import ImagesCartItemSerializer
from rest_framework import exceptions
from .mixins import MethodSerializerView


class CartDetail(RetrieveAPIView):
    def get_object(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            obj = get_object_or_404(Cart,user=user,active=True)
            
            return obj
        else:
            try:
                device_id = self.request.headers['deviceid']
            except:
                raise NotFound({"detail":"user not found"})
            guestuser ,created=GuestUsers.objects.get_or_create(device_id=device_id)
            obj ,created = Cart.objects.get_or_create(device_id=guestuser.device_id ,active=True)
            return obj
    serializer_class = CartSerializer

class CartDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user)
        return queryset
    
    serializer_class = CartSerializer


class CartitemList(MethodSerializerView,ListCreateAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:   
            user = self.request.user
            queryset = CartItem.objects.filter(cart__user=user,cart__active=True)
            return queryset
        else:
            
            try:
                device_id = str(self.request.headers['deviceid'])  
            except:
                raise NotFound({"detail":"user not found"})
            guestuser ,created=GuestUsers.objects.get_or_create(device_id=device_id)
            queryset = CartItem.objects.filter(cart__device_id=guestuser)
            return queryset
    method_serializer_classes = {
        ('GET', ): CartItemSerializer,
        ('POST'): CreateCartItemSerializer
    }
    #serializer_class = CartItemSerializer
   
    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            type = str(request.data['item_type'])
        except Exception as e:
            raise ValidationError("Please Enter a type")

        try:
            item_id = int(request.data['item_id'])
        except Exception as e:
            raise ValidationError("Please Enter a item_id")
        if type == 'product':
            item = get_object_or_404(Product, pk=item_id)
            cartitem = self.get_queryset().filter(item_product=item)
           

        elif type == 'article':
            item = get_object_or_404(Article, pk=item_id)
            cartitem = self.get_queryset().filter(item_article=item)

        elif type == 'pack':
            item = get_object_or_404(Pack, pk=item_id)
            cartitem = self.get_queryset().filter(item_pack=item)

        elif type == 'custompack':
            item = get_object_or_404(CustomPack, pk=item_id)
            cartitem = self.get_queryset().filter(item_custompack=item)
        else:
            return Response("not a valid type", status=status.HTTP_400_BAD_REQUEST)
        if cartitem.exists():
            cartitem = cartitem.first()
            cartitem.quantity += 1
            cartitem.save()
        else:
            if self.request.user.is_authenticated:
                cart = get_object_or_404(Cart, user=request.user ,active=True)
                
            else:
                
                try:
                    device_id = str(self.request.headers['deviceid'])
         
                except:
                    raise NotFound({"detail":"user not found"})

                guestuser=get_object_or_404(GuestUsers,pk=device_id)
                cart , created = Cart.objects.get_or_create(device_id=guestuser,defaults = {'user': None})

            cartitem = CartItem(cart=cart, item=item)
            cartitem.save()
        if type == 'custompack' :
            item.inCart=True
            item.save()
        print(cartitem)
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartitemListDelete(MethodSerializerView,RetrieveUpdateDestroyAPIView):
    serializer_class=CartItemSerializer
    method_serializer_classes = {
        ('GET', ): CartItemSerializer,
        ('PUT'): UpdateCartItemSerializer
    }
    def get_queryset(self):
        if self.request.user.is_authenticated:   
            user = self.request.user
            queryset = CartItem.objects.filter(cart__user=user)
            return queryset
        else:
            try:
                print(self.request.headers['deviceid'])
                device_id = self.request.headers['deviceid']
            except:
                raise NotFound({"detail":"user not found"})
            guestuser ,created=GuestUsers.objects.get_or_create(device_id=device_id)
            queryset = CartItem.objects.filter(cart__device_id=guestuser)
            return queryset
    def update(self, request, *args, **kwargs):
        cartitem = self.get_object()
        serializer = UpdateCartItemSerializer(cartitem , data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data,status=status.HTTP_200_OK)
  
    

class CartLenght(ListAPIView):
    permission_classes =[IsAuthenticated]
    def get_queryset(self):
        queryset = CartItem.objects.filter(cart__user=self.request.user ,cart__active=True)
        return queryset
    def list(self, request, *args, **kwargs):
        cartitems=self.get_queryset()
       
        return Response (len(cartitems),status=status.HTTP_200_OK)




   

