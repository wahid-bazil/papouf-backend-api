
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    #Product
    path('product', ImagesProductList.as_view()),
    path('product/<int:pk>', ImagesProductDetail.as_view()),
    path('product/category-products/<str:title>', ImagesProductCategoryDetails.as_view()),
    path('product/filter-products/<str:title>', ImagesProductFilterDetails.as_view()),

    #Pack
    #path('pack', ImagesPackList.as_view()),
    path('pack/<int:pk>', ImagesPacktDetail.as_view()),
    path('pack/category-items/<str:title>', ImagesPackCategoryDetails.as_view()),
    path('pack/filter-products/<str:title>', ImagesPacktFilterDetails.as_view()),
    
  



    path('collection',ImagesCollectionList.as_view()),
    #path('pack/category/<str:pk>', ImagesPackCategoryDetails.as_view()),

    path("cartitems",ImagesCartitemList.as_view()),
    path("boxe",ImagesBoxeList.as_view()),
    path("article",ImagesBoxeList.as_view()),
    path("article/<str:title>",ImagesArticleCategoryDetails.as_view()),
    path("article-childen/<int:pk>",ImagesArticleChildrenList.as_view()),
    path("boxe/<int:pk>",ImagesBoxeDetail.as_view()),
    path("custompack",ImagesCustomPackList.as_view()),
    path("custompack/user-images/<int:pk>",UserImagesCustomPack.as_view()),
    path("custompackarticle",ImagesCustomPackArticlesDetail.as_view()),
    path("userimages/custompack",ImagesCustomPackUserImagesList.as_view()),
    path("userimages/custompack/<int:pk>",ImagesCustomPackUserImagesDetail.as_view()),
    path("userimage/<int:pk>",ImagesUserImageDetail.as_view()),
    path("order/<int:pk>",ImagesOrderDetal.as_view())
]   