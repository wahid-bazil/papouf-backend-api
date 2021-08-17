from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
        #Products
    path('product/categories', ProductCategorylist.as_view()),
    path('product/category-filters/<str:title>', ProductCategoryDetailsFliterList.as_view()),
    path('product/category-products/<str:title>' , ProductCategoryDetails.as_view()),
    path('product/filter-products/<str:title>' , ProductFilterDetails.as_view()),

    #Packs
    path('pack/categories', PackCategorylist.as_view()),
    path('pack/category-filters/<str:title>', PackCategoryDetailsFliterList.as_view()),
    path('pack/category-products/<str:title>' , PackCategoryDetails.as_view()),
    path('pack/filter-products/<str:title>' , PackFilterDetails.as_view()),
    





    
    path('article/categories', ArticleCategorylist.as_view()),
    path('pack/<str:pk>', PackCategoryDetails.as_view()),
    path('images/product/<str:pk>', ImagesProductCategoryDetails.as_view()),
    
    path('article/<str:pk>', ArticleCategoryDetails.as_view()),

    
   
]
"""




"""