from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ShippingRegion)
admin.site.register(models.ShippingCity)
admin.site.register(models.ShippingDelay)
admin.site.register(models.ShippingHandler)
admin.site.register(models.ShippingMode)
admin.site.register(models.ShippingNetPrice)
admin.site.register(models.IntervalOrderToltal)

