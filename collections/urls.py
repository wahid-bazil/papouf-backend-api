from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('product/<int:pk>', ProductDetail.as_view()),
    path('pack/<int:pk>', PackDetail.as_view()),
    path('product', ProductList.as_view()),
    path('featured/product', FeaturedProductList.as_view()),
    path('featured/pack', FeaturedPackList.as_view()),
 
    path('article-children/<int:pk>',ArticleChildrendList.as_view())
]
