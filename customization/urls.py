from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from customization.views import *


urlpatterns = [

  path('custompack', CustomPackList.as_view()),
  path('custompack/<int:pk>', CustomPackDetails.as_view()),
  path('custompack/pack-copy', PackCopyCustomisation.as_view()),
  path('custompack/packitems',CustomPackArticleList.as_view()),
  path('custompack/packitems/<int:pk>',CustomPackArticleDetail.as_view()),


  
  
  
  
 
    
]
""" path('Boxes', BoxestList.as_view()),
    path('Boxes/<int:pk>',BoxeDetail.as_view()),
    path('Articles', ArticlestList.as_view()),
    path('Articles/<int:pk>',ArticleDetail.as_view()),
    path('Articles/category',Article_category_List.as_view()),
    path('customized_boxe',Customized_product_view.as_view()),
    path('add',Customized_product_art_list.as_view()),
    path('update/<int:pk>',Customized_product_art_detail.as_view())"""