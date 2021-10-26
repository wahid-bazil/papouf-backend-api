from os import stat
from django.db.models import query
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializers import *
from media.serializers import ImagesProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


#Products

class ProductCategoryMiniDetail(generics.RetrieveAPIView):
    queryset=ProductCategory.objects.all()
    serializer_class = ProductCategoryMiniSerializer
    lookup_field = 'slug'
class ProductCateogoriesTree(generics.ListAPIView):
    def get_queryset(self):
        main_categories = ProductCategory.objects.filter(parent=None)  #get only the parents categories and then serialize them to return A json tree
        return main_categories
    serializer_class=ProductCategoriesTreeSerializer
    pagination_class = StandardResultsSetPagination

class ProductCateogoryChildrenTree(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class=ProductCategoriesTreeSerializer

class ProductCategoryItems(generics.ListAPIView):
    def get_queryset(self):
        category_slug =self.kwargs.get('slug')
        category = get_object_or_404(ProductCategory ,slug=category_slug)
        category_children = category.get_children()
        categoryitems=PackCategoryItem.objects.none()
        products=Pack.objects.none()
        filter_label = self.request.query_params.get('filter')
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
    serializer_class = ProductSerializer
    pagination_class =StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend ,filters.OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = ['sale_price' ,'title','created','orders']



class ProductflitredList(generics.ListAPIView):
    def get_queryset(self):
        product_category_items= ProductCategoryItem.objects.filter(productcategory__label=self.kwargs.get('category') , filter__label=self.kwargs.get('filter'))
        queryset =[]
        for element in product_category_items:
            queryset.append(element.product)
        return queryset
    serializer_class = ProductSerializer
      

#Packs
class PackCategoryMiniDetail(generics.RetrieveAPIView):
    queryset=PackCategory.objects.all()
    serializer_class = PackCategoryMiniSerializer
    lookup_field = 'slug'
class PackCateogoriesTree(generics.ListAPIView):
    def get_queryset(self):
        main_categories = PackCategory.objects.filter(parent=None)  #get only the parents categories and then serialize them to return A json tree
        return main_categories
    serializer_class=PackCategoriesTreeSerializer

class PackCateogoryChildrenTree(generics.RetrieveAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=PackCategoriesTreeSerializer 

class PackCategoryItems(generics.ListAPIView):
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
        
    serializer_class = PackSerializer
    pagination_class =StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend ,filters.OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = ['sale_price' ,'title','created','orders']





    


class PackflitredList(generics.ListAPIView):
    def get_queryset(self):
        pack_category_items = PackCategoryItem.objects.filter(packcategory__label=self.kwargs.get('category') , filter__label=self.kwargs.get('filter'))
        queryset=[]
        for element in pack_category_items:
            queryset.append(element.pack)
        return queryset
    serializer_class = PackSerializer

class PackArticlesCategoriesList(generics.RetrieveAPIView):
    queryset = PackCategory.objects.all()
    serializer_class = PackArticlesCategoriesSerializer
    lookup_field ='label'
    



#Articles

class ArticleCateogoriesList(generics.ListAPIView):
    queryset=ArticleCategory.objects.all() 
    serializer_class=ArticleCategoryMiniSerializer

class ArticleCateogoryChildrenTree(generics.RetrieveAPIView):
    queryset = PackCategory.objects.all()
    serializer_class=ArticleCategoriesTreeSerializer 

class ArticleCategoryItems(generics.ListAPIView):
    def get_queryset(self):
        category_slug =self.kwargs.get('slug')
        print(category_slug)
        queryset = Article.objects.none()
        categoryitems = ArticleCategoryItem.objects.filter(articlecategory__slug=category_slug)
        print('here' ,categoryitems)
        for element in categoryitems:
            queryset = queryset | Article.objects.filter(pk=element.article.pk)
        return queryset
    serializer_class = ArticleSerializer
    

    






























