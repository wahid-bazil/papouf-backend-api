from django.contrib import admin
from . import models
# Register your models here.


class PaymentModeAdmin(admin.ModelAdmin):
    model = models.PaymentMode
    
    list_display = ('id', 'title', 'slug')

