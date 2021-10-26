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
from .mixins import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters





class ImagesCartitemList(generics.ListAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CartItem.objects.filter(
                cart__user=user, cart__active=True)
            return queryset
        else:
            try:
                  device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            queryset = CartItem.objects.filter(cart__device_id=guestuser ,cart__active=True)
            return queryset
    serializer_class = ImagesCartItemSerializer





class ImagesArticleList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ImagesArticleSerializer

class ImagesArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ImagesArticleSerializer


class ImagesArticleChildrenList(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        children=obj.get_children()
        children.insert(0,obj)
        serializer = ImagesArticleSerializer(children,many=True ,context={"request":request})
        return Response(serializer.data,status.HTTP_200_OK)


        




"""CustomPack"""
class ImagesCustomPackDetail(generics.RetrieveAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CustomPack.objects.filter(user=user)
            return queryset
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            queryset = CustomPack.objects.filter(
                device_id=guestuser)
            return queryset
    serializer_class =ImagesCustomPackSerializer


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




class ImagesFeaturedProductList(generics.ListAPIView):
    def  get_queryset(self):
        queryset = Product.objects.filter(status__title="featured")
        return queryset
    serializer_class = ImagesProductSerializer
    pagination_class = StandardResultsSetPagination
    def get_serializer_context(self):
        context={"request": self.request}
        return context
        
class ImagesFeaturedPackList(generics.ListAPIView):
    def  get_queryset(self):
        queryset = Pack.objects.filter(status__title="featured")
        return queryset
    serializer_class = ImagesPackSerializer
    pagination_class = StandardResultsSetPagination 
    def get_serializer_context(self):
        context={"request": self.request}
        return context
    
    
     
 




class ImagesProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ImagesProductSerializer

class ImagesPacktDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pack.objects.all()
    serializer_class = ImagesPackSerializer

#ProductCategory
class ImagesProductCategoryDetails(generics.ListAPIView):
    def get_queryset(self):
        category_slug =self.kwargs.get('slug')
        category = get_object_or_404(ProductCategory , slug =category_slug )
        category_children = category.get_children()
        filter_label = self.request.query_params.get('filter')
        categoryitems=ProductCategory.objects.none()
        products=Pack.objects.none()
        if filter_label :
            filter = get_object_or_404(Filter , slug =filter_label)
            for element in category_children :
                categoryitems = categoryitems | element.productcategoryitem_set.filter(filter=filter)
        else :
            for element in category_children :
                categoryitems = categoryitems | element.productcategoryitem_set.all()
        for element in categoryitems :
            products = products | Product.objects.filter(pk=element.product.id)
        return products
    serializer_class = ImagesProductSerializer
    pagination_class =StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend ,filters.OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = ['sale_price' ,'title','created','orders']


    
#PackCategory
class ImagesPackCategoryDetails(generics.ListAPIView):
    def get_queryset(self):
        category_slug =self.kwargs.get('slug')
        category = get_object_or_404(PackCategory , slug =category_slug )
        category_children = category.get_children()
        filter_label = self.request.query_params.get('filter')
        categoryitems=PackCategoryItem.objects.none()
        packs=Pack.objects.none()
        if filter_label :
            filter = get_object_or_404(Filter , slug =filter_label)
            for element in category_children :
                categoryitems = categoryitems | element.packcategoryitem_set.filter(filter=filter)
        else :
            for element in category_children :
                categoryitems = categoryitems | element.packcategoryitem_set.all()
        
        for element in categoryitems :
            packs = packs | Pack.objects.filter(pk=element.pack.id)
        return packs
    serializer_class = ImagesPackSerializer
    pagination_class =StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend ,filters.OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = ['sale_price' ,'title','created','orders']



# Order

class ImagesOrderDetal(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class=ImagesOrderSerializer


#articles 
class ImagesArticleCategoryItems(generics.ListAPIView):
    def get_queryset(self):
        category_slug =self.kwargs.get('slug')
        queryset = Article.objects.none()
        categoryitems = ArticleCategoryItem.objects.filter(articlecategory__slug=category_slug)
        for element in categoryitems:
            queryset = queryset | Article.objects.filter(pk=element.article.pk)
        return queryset
    serializer_class = ImagesArticleSerializer
    