
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from delivery.views import *


urlpatterns = [
 
    path("delay-cost",ShippingDelayCost.as_view()),
    path('cities',ShippingCityList.as_view()),
    path('regions',ShippingRegionList.as_view()),
    path('region-cites/<str:title>',ShippingRegionDetails.as_view()),
    path("shippingmode",ShippingModeList.as_view())


    

  
        
]
