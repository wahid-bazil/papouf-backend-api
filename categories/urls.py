from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    #Products
    path('product/category-description/<str:slug>', ProductCategoryMiniDetail.as_view()),
    path('product/categories', ProductCateogoriesTree.as_view()),
    path('product/category-children/<int:pk>', ProductCateogoryChildrenTree.as_view()),
    path('product/category-items/<str:slug>' , ProductCategoryItems.as_view()),
    
 

    #Packs
    path('pack/category-description/<str:slug>', PackCategoryMiniDetail.as_view()),
    path('pack/categories', PackCateogoriesTree.as_view()),
    path('pack/category-children/<int:pk>', PackCateogoryChildrenTree.as_view()),
    path('pack/category-items/<str:slug>' , PackCategoryItems.as_view()),
    path('articles-categories/pack/<str:slug>',PackArticlesCategoriesList.as_view()),


    #Articles
    path('article/category-items/<str:slug>', ArticleCategoryItems.as_view()),
    path('article/categories', ArticleCateogoriesList.as_view()),

    
    





    


    
   
]
