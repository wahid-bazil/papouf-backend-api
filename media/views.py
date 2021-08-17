from django.db.models import query
#from Orders.models import Order
#from category.models import ArticleCategory
from media.models import BoxeImage, ProductImage
from django.shortcuts import render

from django.db.models.query import QuerySet
from customization.models import CustomPackArticle
from products.models import Article, Boxe, Pack, Product
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AND, SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import GuestUsers
from products.serializers import PackSerializer
from categories.models import *
from .serializers import *
from rest_framework.views import APIView
from orders.models import *

class UserImagesCustomPack(generics.RetrieveAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CustomPack.objects.filter(user=user)

            return queryset
        else:
            try:
                device_id = str(self.request.COOKIES['device_id'])
            except:
                raise NotFound({"detail": "user not found"})
            queryset = CustomPack.objects.filter(device_id=device_id)
            return queryset

    serializer_class = UserImagesCustomPackSerializer


class ImagesCartitemList(generics.ListAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CartItem.objects.filter(
                cart__user=user, cart__active=True)
            return queryset
        else:
            try:
                device_id = str(self.request.COOKIES['device_id'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            queryset = CartItem.objects.filter(cart__device_id=guestuser)
            return queryset
    serializer_class = ImagesCartItemSerializer


class ImagesBoxeList(generics.ListAPIView):
    queryset = Boxe.objects.all()
    serializer_class = ImagesBoxeSerializer


class ImagesArticleList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ImagesArticleSerializer

"""
class ImagesArticleCategoryDetails(generics.RetrieveAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class = ImagesArticleCategorySerializer
"""
class ImagesArticleChildrenList(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        children=obj.get_children()
        children.insert(0,obj)
        serializer = ImagesArticleSerializer(children,many=True ,context={"request":request})
        return Response(serializer.data,status.HTTP_200_OK)


        

class ImagesBoxeDetail(generics.RetrieveAPIView):
    queryset = Boxe.objects.all()
    serializer_class = ImagesBoxeSerializer


"""CustomPack"""
class ImagesCustomPackList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = CustomPackImage.objects.all()
    serializer_class = ImagesCustomPSerializer
    def create(self, request, *args, **kwargs):
        CustomPackImage.objects.filter(item__isCopy=False).delete()
        return super().create(request, *args, **kwargs)



class ImagesCustomPackArticlesDetail(generics.ListAPIView):
    def get_queryset(self):
        custompack_id = self.request.query_params.get('id')
        print(custompack_id)
        queryset = CustomPackArticle.objects.filter(custompack__id=custompack_id)
        return queryset
    serializer_class = ImagesCustomPackArticleSerializer

class ImagesCustomPackUserImagesList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = CustomPackUserImage.objects.all()
    serializer_class = CustomPackImageSerializer


class ImagesCustomPackUserImagesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomPack.objects.all()
    serializer_class = ImagesCustomPackUserImagesSeriazer


class ImagesUserImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomPackUserImage.objects.all()
    serializer_class =ImagesCustomPackUserImageSeriazer

""" variation"""
class ImagesProductList(generics.ListAPIView):
    def get_queryset(self):
        status=self.request.query_params.get('status')
        if status :
            queryset=Product.objects.filter(status=status)
        else :
            queryset=Product.objects.all()
        return queryset
    serializer_class = ImagesProductSerializer



class ImagesCollectionList(APIView):
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
        products_serializer=ImagesProductSerializer(products,many=True ,context={"request":request})
        pack_serializers=ImagesPackSerializer(packs,many=True ,context={"request":request})
        data=pack_serializers.data + products_serializer.data
        return Response(data)
     
 




class ImagesProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ImagesProductSerializer

class ImagesPacktDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pack.objects.all()
    serializer_class = ImagesPackSerializer

#ProductCategory
class ImagesProductCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ImagesProductCategorySerializer
    lookup_field ='title'  
    def get_serializer_context(self):
        context={"request": self.request}
        return context

class ImagesProductFilterDetails(generics.RetrieveUpdateAPIView):
    queryset = ProductCategoryFilter.objects.all()
    serializer_class = ImagesProductFilterSerializer
    lookup_field = 'title'
    
#PackCategory
class ImagesPackCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=ImagesPackCategorySerializer
    lookup_field ='title'
    def get_serializer_context(self):
        context={"request": self.request}
        return context

class ImagesPacktFilterDetails(generics.RetrieveUpdateAPIView):
    queryset = PackCategoryFilter.objects.all()
    serializer_class = ImagesPackFilterSerializer
    lookup_field = 'title'

# Order

class ImagesOrderDetal(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class=ImagesOrderSerializer