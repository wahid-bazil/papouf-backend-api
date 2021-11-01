from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from orders.views import *


urlpatterns = [
path('list', OrderList.as_view()),
path('list/<int:pk>', OrderDetail.as_view()),
path('nb-of-orders',OrdersLenght.as_view())

]
