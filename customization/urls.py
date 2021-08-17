from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from customization.views import *


urlpatterns = [
  
  path('test',test.as_view()),
  path('userCustomPack', CustomPackList.as_view()),
  path('userCustomPack/<int:pk>', CustomPackDetails.as_view()),
  path('userCustomPack/pack-copy', PackCopyCustomisation.as_view()),
  path('userCustomPack/detail', CustomPackDetail.as_view()),
  path('userCustomPack/packitems',CustomPackArticleList.as_view()),
  path('userCustomPack/packitems/<int:pk>',CustomPackArticleDetail.as_view()),
  path('userCustomPack/images/upload', CustomPackImageList.as_view()),
  path('userCustomPack/images/update/<int:pk>', CustomPackImageDetail.as_view()),
  path('userCustomPack/uimage/<int:pk>', CustomPackBoxeImageView.as_view()),
  path('custompack/total/<int:pk>', CustomPackTotal.as_view()),
  
  
  
  
 
    
]
""" path('Boxes', BoxestList.as_view()),
    path('Boxes/<int:pk>',BoxeDetail.as_view()),
    path('Articles', ArticlestList.as_view()),
    path('Articles/<int:pk>',ArticleDetail.as_view()),
    path('Articles/category',Article_category_List.as_view()),
    path('customized_boxe',Customized_product_view.as_view()),
    path('add',Customized_product_art_list.as_view()),
    path('update/<int:pk>',Customized_product_art_detail.as_view())"""