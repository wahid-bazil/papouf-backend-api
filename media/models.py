
from django.db import models
from django.utils.translation import gettext_lazy as _
from categories.models import ArticleCategory
from products.models import *
from delivery.models import ShippingBox
# Create your models here.


def upload_to(instance, filename):
    if instance._meta.verbose_name == "productimage":
        return 'products/{filename}'.format(filename=filename)
    elif instance._meta.verbose_name == "packimage":
        return 'packs/{filename}'.format(filename=filename)
  
    elif instance._meta.verbose_name == "articleimage":
        return 'articles/{filename}'.format(filename=filename)
    elif instance._meta.verbose_name == "boxeimage":
        return 'boxes/{filename}'.format(filename=filename)
    elif instance._meta.verbose_name == "custompackimage":
        return 'custompacks/{filename}'.format(filename=filename)         
    elif instance._meta.verbose_name == "shippingbox":
        return 'shippingBox/{filename}'.format(filename=filename)
    elif instance._meta.verbose_name == "articlecategoryimage":
        return 'articlecategory/{filename}'.format(filename=filename)
    

    
class ArticleCategoryImage(models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE ,related_name='images')
    class Meta :
        verbose_name = 'articlecategoryimage'

class ProductImage (models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey(Product, on_delete=models.CASCADE ,related_name='images')
    class Meta :
        verbose_name = 'productimage'

class PackImage (models.Model):
    main_image = models.BooleanField(default=False )
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey(Pack,on_delete=models.CASCADE , related_name='images')

    class Meta :
        verbose_name = 'packimage'


class BoxeImage (models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey(Boxe,on_delete=models.CASCADE,related_name='images')
    class Meta :
        verbose_name = 'boxeimage'


class ArticleImage (models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey(Article,on_delete=models.CASCADE ,related_name='images')
    class Meta :
        verbose_name = 'articleimage'


class CustomPackImage (models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey('customization.CustomPack',on_delete=models.CASCADE ,related_name='main_image')
    class Meta :
        verbose_name = 'custompackimage'

class ShippingBoxImage (models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    item = models.ForeignKey(ShippingBox,on_delete=models.CASCADE,related_name='images')
    class Meta :
        verbose_name = 'shippingbox'

