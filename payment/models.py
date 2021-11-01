from django.db import models
from django.template.defaultfilters import slugify, title
# Create your models here.


class PaymentMode(models.Model):
    title = models.CharField(max_length=30 , unique=True)
    description=  models.CharField(max_length=150)
    slug = models.CharField(blank=True , max_length=30)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(PaymentMode, self).save(
            force_insert, force_update, *args, **kwargs)
    
    def __str__(self):
        return self.title