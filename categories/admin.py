from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ProductCategory)
admin.site.register(models.PackCategory)
admin.site.register(models.ArticleCategory)
#admin.site.register(models.PackType)
admin.site.register(models.ProductCategoryFilter)
admin.site.register(models.PackCategoryFilter)