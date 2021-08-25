
#from category.models import PackType
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone, tree
from users.models import NewUser, GuestUsers
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from products.models import Article, Boxe
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from cart.models import CartItem
from media.models import BoxeImage, CustomPackImage


def upload_to(instance, filename):

    return 'custompacks/{filename}'.format(filename=filename)

class CustomPack (models.Model):
    isCopy = models.BooleanField(default=False)
    inCart = models.BooleanField(default=False)
    title = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(
        NewUser, on_delete=models.CASCADE, null=True, blank=True)
    cost_price = models.DecimalField(
        decimal_places=2, max_digits=20, default=0)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=20, default=0,)
    boxe = models.ForeignKey(
        Boxe, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(Article, through='CustomPackArticle')
    device_id = models.ForeignKey(
        GuestUsers, on_delete=models.CASCADE, blank=True, null=True)
    cartItem = GenericRelation(CartItem, related_query_name='item_custompack')
    #pack_type = models.ForeignKey(PackType , on_delete=CASCADE, blank=True , null=True)
    
    class Meta:
        unique_together = ('user', 'device_id',)

    class Meta:
        verbose_name = 'custompack'

    def get_sale_price(self):
        return self.sale_price

    def get_cost_price(self):
        return self.cost_price

    def update_sale_price(self):
        sale_price = 0
        items = self.custompackarticle_set.all()
        for item in items:
            sale_price += item.item.get_sale_price()*item.quantity
        images = self.user_images.all()

        for image in images:
            sale_price += image.total
        self.sale_price = sale_price
        self.save()

    def update_cost_price(self):
        cost_price = 0
        items = self.custompackarticle_set.all()
        for item in items:
            cost_price += item.item.get_cost_price()*item.quantity
        images = self.user_images.all()
        for image in images:
            cost_price += image.total
        self.cost_price = cost_price
        self.save()

    def update_nb_items(self):
        nb = self.custompackarticle_set.all().count()
        self.nb_items = nb
        self.save()

    def get_prix(self):
        return self.prix



class CustomPackArticle(models.Model):
    custompack = models.ForeignKey(CustomPack, on_delete=models.CASCADE )
    item = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def update_total(self):
        sale_price = self.item.get_sale_price()
        total = sale_price*self.quantity
        self.total = total

    class Meta :
        verbose_name = 'packarticle'    


class CustomPackUserImage(models.Model):
    custompack = models.ForeignKey(
        CustomPack, on_delete=models.CASCADE, related_name='user_images', null=True)
    image = models.ImageField(
        _("Image"), upload_to=upload_to, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=3)


class CustomPackSetting(models.Model):
    is_active = models.BooleanField(default=False)
    default_boxe = models.ForeignKey(Boxe, on_delete=models.CASCADE)
    image_sale_price = models.PositiveIntegerField()
    maxNb_Of_images = models.PositiveIntegerField()

@receiver(post_save, sender=CartItem)
def CreateCustompack(sender, instance, created, **kwargs):
    if instance.item._meta.verbose_name == 'custompack':
        if created:
            if instance.item.user :
                CustomPack.objects.create(user=instance.item.user)
            else :
                CustomPack.objects.create(device_id=instance.item.device_id)


   



@receiver(pre_save, sender=CustomPackUserImage)
def CustomPackImage_pre_save(sender, instance, **kwargs):
    setting = CustomPackSetting.objects.filter(is_active=True).first()
    sale_price=setting.image_sale_price
    instance.total = instance.quantity*sale_price
    


@receiver(post_save, sender=CustomPackUserImage)
def CustomPackImage_post_save(sender, instance, **kwargs):
    instance.custompack.update_sale_price()
    instance.custompack.save()


@receiver(pre_save, sender=CustomPackArticle)
def CustomPackArticle_pre_save(sender, instance, **kwargs):
    instance.update_total()


@receiver(post_save, sender=CustomPackArticle)
def CustomPackArticle_post_save(sender, instance, **kwargs):
    instance.custompack.update_sale_price()
    instance.custompack.update_cost_price()
    instance.custompack.update_nb_items()


@receiver(post_delete, sender=CustomPackArticle)
def CustomPackArticle_post_delete(sender, instance, **kwargs):
    instance.custompack.update_sale_price()
    instance.custompack.update_cost_price()
    instance.custompack.update_nb_items()


@receiver(post_save, sender=CustomPack)
def customized_product_is_created(sender, update_fields, instance, created, **kwargs):
    if created and instance.isCopy == False:
        setting = CustomPackSetting.objects.filter(is_active=True).first()
        instance.boxe = setting.default_boxe
        #image = instance.boxe.images.filter(for_custompack=True).first().image
        #CustomPackImage.objects.create(item=instance, image=image)
        instance.title = "pack_"+str(instance.id)
        instance.save()



"""@receiver(post_save, sender=GuestUsers)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        CustomPack.objects.create(device_id=instance)


"""