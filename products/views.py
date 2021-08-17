
import collections
from media.models import BoxeImage
from rest_framework.fields import MultipleChoiceField
from products.models import Boxe, Pack, Product, test
from products.serializers import ArticleSerializer, BoxeSerializer, PackSerializer, ProductSerializer, testArticleSerializer, testSerializer
from rest_framework import generics, serializers 
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView

  
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from django.utils.translation import ugettext_lazy as _


from products.models import Product , Article
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser,FormParser
from media.serializers import ImagesProductSerializer




class testlist(generics.ListCreateAPIView):
    def get_queryset(self):
        print(self.kwargs.get('case'))
        return test.objects.all()
    serializer_class = testSerializer



class testArticle(generics.ListCreateAPIView):
    queryset=Article.objects.all()
    serializer_class=testArticleSerializer

class BoxeList(generics.ListCreateAPIView):
    queryset =  Boxe.objects.all()
    serializer_class = BoxeSerializer



class ProductList(generics.ListCreateAPIView):
    def get_queryset(self):
        status=self.request.query_params.get('status')
        if status :
            queryset=Product.objects.filter(status=status)
        else :
            queryset=Product.objects.all()
        return queryset
    serializer_class = ProductSerializer

class CollectionList(APIView):
    def get(self, request, *args, **kwargs):
        status=self.request.query_params.get('status')
        nbOfproducts=self.request.query_params.get('nbOfproducts')
        nbOfpacks=self.request.query_params.get('nbOfpacks')
        if nbOfproducts :
            nbOfproducts=int(nbOfproducts)
        if nbOfpacks :
            nbOfpacks=int(nbOfpacks)

        if status :
            products=Product.objects.filter(status=status).order_by('-created')[:nbOfproducts]
            packs = Pack.objects.filter(status=status).order_by('-created')[:nbOfpacks]
        else :
            products=Product.objects.all()
            packs = Pack.objects.all()
        products_serializer=ProductSerializer(products,many=True)
        pack_serializers=PackSerializer(packs,many=True)
        data=pack_serializers.data + products_serializer.data
        return Response(data)
        

class ArticleChildrendList(RetrieveAPIView):
    queryset = Article.objects.all()
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        children=obj.get_children()
        children.insert(0,obj)
        serializer = ArticleSerializer(children,many=True)
        return Response(serializer.data,status.HTTP_200_OK)

    





class PackList(generics.ListCreateAPIView):
    queryset = Pack.objects.all()
    serializer_class = PackSerializer

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ProductDetail(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ImagesProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ImagesProductSerializer


class ArticleDetail(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



class PackDetail(generics.RetrieveUpdateAPIView):
    queryset = Pack.objects.all()
    serializer_class = PackSerializer