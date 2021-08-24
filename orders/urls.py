from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from orders.views import *


urlpatterns = [
path('list', OrderList.as_view()),
path('<int:pk>', OrderDetail.as_view()),
path('detail/lenght',OrdersLenght.as_view())
]
