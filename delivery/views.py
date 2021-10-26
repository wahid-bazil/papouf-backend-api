from rest_framework import generics
from delivery.models import IntervalOrderToltal, ShippingCity, ShippingDelay, ShippingMode, ShippingNetPrice
from cart.models import Cart
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
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError, PermissionDenied
from users.models import  NewUser
from rest_framework.views import APIView
from media.serializers import ImagesCartItemSerializer
from .serializers import *


class ShippingCityList(generics.ListAPIView):
    queryset = ShippingCity.objects.all()
    serializer_class = ShippingCitySerializer


class ShippingRegionList(generics.ListAPIView):
    queryset = ShippingRegion.objects.all()
    serializer_class = ShippingRegionMiniSerializer


class ShippingRegionDetails(generics.RetrieveAPIView):
    queryset = ShippingRegion.objects.all()
    serializer_class = ShippingRegionSerializer
    lookup_field = 'title'


class ShippingModeList(generics.ListAPIView):
    queryset = ShippingMode.objects.all()
    serializer_class = ShippingModeSerializer


class ShippingDelayCost(generics.CreateAPIView):
    serializer_class=ShippingDelayCostSerializer
    def post(self, request, *args, **kwargs):
        city = self.request.data['city']
        total = self.request.data['order_total']
        shipping_mode = self.request.data['shipping_mode']
        city = get_object_or_404(ShippingCity, title=city)
        shipping_mode = get_object_or_404(
            ShippingMode, title=shipping_mode)
        delay_per_hour = ShippingDelay.objects.get(
            cities__in=[city], shipping_mode=shipping_mode).delay_per_hour
        total_order_interval = IntervalOrderToltal.objects.get(
            min_total__lte=total, max_total__gte=total, shipping_mode=shipping_mode)
        shipping_price = ShippingNetPrice.objects.get(
            shipping_mode=shipping_mode, total_order_interval=total_order_interval, cities__in=[city]).net_shipping_price
        return Response({'delay_per_hour': delay_per_hour, 'shipping_price': shipping_price}, status=status.HTTP_200_OK)



