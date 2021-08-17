from django.contrib import admin
from . import models

admin.site.register(models.CustomPack)
admin.site.register(models.CustomPackArticle)
admin.site.register(models.CustomPackSetting)
admin.site.register(models.CustomPackUserImage)


