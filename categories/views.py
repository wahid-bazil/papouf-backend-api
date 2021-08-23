from os import stat
from django.db.models import query
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from media.serializers import ImagesProductSerializer
from rest_framework.response import Response
from rest_framework import status

class ProductCateogoryList(generics.ListAPIView):
    def get_queryset(self):
        main_categories = ProductCategory.objects.filter(parent=None)
        return main_categories
    serializer_class=ProductCategoryChildrenSerializer

class ProductCateogoryChildrenList(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ProductCategoryChildrenSerializer
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
"""class PackTypeMainCategoriesList(generics.RetrieveAPIView):
    queryset= PackType.objects.all()
    serializer_class=PackTypeSerializer
 """   

class PackCateogoryChildrenList(generics.RetrieveAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=PackCategoryChildrenSerializer



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


class PackArticleCategoryList(generics.RetrieveUpdateAPIView):
    queryset = PackCategory.objects.all()
    serializer_class = PackArticleCategorySerializer
    lookup_field ='title'
    











class ImagesProductCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ImagesProductCategorySerializer




class ArticleCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class=ArticleCategoryItemsSerializer
    lookup_field = 'title'




class PackCategorylist(generics.ListCreateAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=PackCategoryMiniSerializer

"""
class ArticleCategorylist(generics.ListCreateAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class=ArticleCategoryMiniSerializer   

"""
"""Category test"""


