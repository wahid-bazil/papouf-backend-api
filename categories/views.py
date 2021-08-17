from os import stat
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from media.serializers import ImagesProductSerializer
from rest_framework.response import Response
from rest_framework import status

class ProductCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ProductCategorySerializer
    lookup_field = 'title'

class ProductFilterDetails(generics.RetrieveAPIView):
    queryset = ProductCategoryFilter.objects.all()
    serializer_class = ProductCategoryFilterSerializer
    lookup_field = 'title'

class ProductCategoryDetailsFliterList(generics.RetrieveUpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ProductCategoryFilterListSerializer
    lookup_field = 'title'

"""Pack"""
class PackCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=PackCategorySerializer
    lookup_field = 'title'

class PackFilterDetails(generics.RetrieveAPIView):
    queryset = PackCategoryFilter.objects.all()
    serializer_class = PackCategoryFilterSerializer
    lookup_field = 'title'

class PackCategoryDetailsFliterList(generics.RetrieveUpdateAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=PackCategoryFilterListSerializer
    lookup_field = 'title'











class ImagesProductCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ImagesProductCategorySerializer




class ArticleCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class=ArticleCategorySerializer


class ProductCategorylist(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ProductCategoryMiniSerializer

class PackCategorylist(generics.ListCreateAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=PackCategoryMiniSerializer


class ArticleCategorylist(generics.ListCreateAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class=ArticleCategoryMiniSerializer   


"""Category test"""


