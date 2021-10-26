
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    #Product
    path('product', ImagesProductList.as_view()),
    path('product/<int:pk>', ImagesProductDetail.as_view()),
    path('product/category-items/<str:slug>', ImagesProductCategoryDetails.as_view()),
    #path('product/<str:category>/<str:filter>' , ImagesProductflitredList.as_view()),

    #Pack
    path('pack/<int:pk>', ImagesPacktDetail.as_view()),
    path('pack/category-items/<str:slug>', ImagesPackCategoryDetails.as_view()),
  
    #featured
    path('featured/product',ImagesFeaturedProductList.as_view()),
    path('featured/pack',ImagesFeaturedPackList.as_view()),
 
    #Cutomization
    path('custompack/<int:pk>',ImagesCustomPackDetail.as_view()),


    #articles
    path('article/category-items/<str:slug>',ImagesArticleCategoryItems.as_view()),
    path('article/<int:pk>',ImagesArticleDetail.as_view()),

    path("cartitems",ImagesCartitemList.as_view()),
    path("article-childen/<int:pk>",ImagesArticleChildrenList.as_view()),
    path("order/<int:pk>",ImagesOrderDetal.as_view())
]   