
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from cart.views import *


urlpatterns = [
 
    path("cartitems",CartitemList.as_view()),
    path("",CartDetail.as_view()),
    path("detail/<int:pk>",CartDetails.as_view()),
    path("cartitems/<int:pk>",CartitemListDelete.as_view()),
    path("nb-of-items",CartLenght.as_view()),
  
    
    
]

"""path("list/",CartItemAPIView.as_view()),
    path("<int:pk>/",CartItemView.as_view()),
    path("list0/",CartList.as_view()),"""
