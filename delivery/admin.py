from django.contrib import admin
from . import models
# Register your models here.


class ShippingCityAdmin(admin.ModelAdmin):
    model = models.ShippingCity
    
    list_display = ('id', 'title')


class ShippingRegionAdmin(admin.ModelAdmin):
    model = models.ShippingRegion
    
    list_display = ('id', 'title')

class ShippingModeAdmin(admin.ModelAdmin):
    model = models.ShippingMode
    
    list_display = ('id', 'title')

class ShippingRegionAdmin(admin.ModelAdmin):
    model = models.ShippingRegion
    
    list_display = ('id', 'title')

class ShippingDelayAdmin(admin.ModelAdmin):
    model = models.ShippingDelay
    list_display = ('delay_per_hour',)
    list_filter = ('cities',)
class ShippingNetPriceAdmin(admin.ModelAdmin):
    list_filter = ('cities',)
    model = models.ShippingNetPrice
    list_display = ('id', 'total_order_interval'  ,'net_shipping_price')


admin.site.register(models.ShippingRegion ,ShippingRegionAdmin)
admin.site.register(models.ShippingCity ,ShippingCityAdmin)
admin.site.register(models.ShippingDelay ,ShippingDelayAdmin)

admin.site.register(models.ShippingMode ,ShippingModeAdmin)
admin.site.register(models.ShippingNetPrice ,ShippingNetPriceAdmin)
admin.site.register(models.IntervalOrderToltal)

