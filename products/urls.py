from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from products.views import *


urlpatterns = [
    path('product/<int:pk>', ProductDetail.as_view()),
    path('product', ProductList.as_view()),
    path('collection', CollectionList.as_view()),
    path('pack/<int:pk>', PackDetail.as_view()),
    path('images/product/<int:pk>', ImagesProductDetail.as_view()),
    path('boxe', BoxeList.as_view()),
    path('article',testArticle.as_view()),
    path('article-children/<int:pk>',ArticleChildrendList.as_view())
]
