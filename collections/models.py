from cart.models import CartItem
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
#from category.models import   PackType
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _





class Product (models.Model):
    status = models.ForeignKey(ItemStatus,on_delete=models.SET_NULL ,null=True ,blank=True)
    title=models.CharField(max_length=35)
    caption = models.CharField(max_length=50 ,blank=True ,null=True)
    inventory=models.IntegerField()
    created=models.DateTimeField(default=timezone.now)
    active=models.BooleanField(default=True)
    cost_price = models.DecimalField(decimal_places=2, max_digits=20 ,blank=True)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    promo_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    promo_percentage =models.IntegerField(blank=True ,null=True)
    description = models.CharField(max_length=200 , default="")
    provider = models.ForeignKey(Provider,on_delete=models.CASCADE,blank=True, null=True)
    cartItem = GenericRelation(CartItem,related_query_name='item_product')
    promo = models.BooleanField(default=False)
    orders=models.PositiveBigIntegerField(default=0)


    class Meta :
        verbose_name = 'product'
        ordering = ['-orders']


class Pack(models.Model):
	status = models.ForeignKey(ItemStatus,on_delete=models.SET_NULL ,null=True ,blank=True)
	title = models.CharField(max_length=120)
	caption = models.CharField(max_length=50 ,blank=True ,null=True)
	cost_price = models.DecimalField(decimal_places=2, max_digits=20,default=0)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, default=0,)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(default=1)
	items = models.ManyToManyField("Article",through='PackArticle')
	is_customized = models.BooleanField(default=False)
	created=models.DateTimeField(default=timezone.now)
	description = models.TextField(max_length=1500,default="")
	cartItem = GenericRelation(CartItem,related_query_name='item_pack')
	orders=models.PositiveBigIntegerField(default=0)
	promo_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	promo_percentage =models.IntegerField(blank=True ,null=True)
	promo = models.BooleanField(default=False)
	

	class Meta :
		verbose_name = 'pack'
		ordering = ['-orders']





class Article(models.Model):
	title = models.CharField(max_length=120)
	#category = models.ForeignKey(ArticleCategory,on_delete=CASCADE,null=True ,related_name="items")
	cost_price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True)
	provider = models.ForeignKey(Provider,on_delete=models.CASCADE,blank=True, null=True)
	created=models.DateTimeField(default=timezone.now)
	description = models.CharField(max_length=150,default="")
	variant_description = models.CharField(max_length=30 ,blank=True , null=True )
	space = models.IntegerField(null=False)
	parent = models.ForeignKey('Article',on_delete=models.CASCADE , blank=True, null=True , related_name='child')


	class Meta :
		verbose_name = 'article'
		ordering = ['sale_price']
	
	def __str__(self) -> str:
		return self.title

		


class PackArticle(models.Model):
	pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
	item = models.ForeignKey(Article,on_delete=CASCADE , verbose_name="Article")
	quantity = models.IntegerField(default=1)
	total = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)









def packArticle_post_delete_saved_receiver(sender, instance, *args, **kwargs):
	instance.pack.update_nb_items()
	packArticles = PackArticle.objects.filter(pack=instance.pack)
	sale_price=0
	cost_price=0
	for packArticle in packArticles :
		sale_price += packArticle.item.get_sale_price()*packArticle.quantity
		cost_price += packArticle.item.get_cost_price()*packArticle.quantity
	instance.pack.sale_price=sale_price
	instance.pack.cost_price=cost_price
	instance.pack.save()

def packArticle_pre_saved_receiver(sender, instance,  *args, **kwargs):
	instance.update_total()

def product_presaved_receiver(sender, instance,  *args, **kwargs):
	if instance.promo:
		if instance.promo_percentage == None:
			promo_percentage=-(((instance.promo_price*100)/instance.sale_price)-100)
			instance.promo_percentage=promo_percentage
		elif  instance.promo_price == None:
			promo_price=(-(instance.promo_percentage-100)*instance.sale_price)/100
			instance.promo_price=promo_price

def pack_presaved_receiver(sender, instance,  *args, **kwargs):
	if instance.promo:
		if instance.promo_percentage == None:
			promo_percentage=-(((instance.promo_price*100)/instance.sale_price)-100)
			instance.promo_percentage=promo_percentage
		elif  instance.promo_price == None:
			promo_price=(-(instance.promo_percentage-100)*instance.sale_price)/100
			instance.promo_price=promo_price

pre_save.connect(product_presaved_receiver, sender=Product)
pre_save.connect(pack_presaved_receiver, sender=Pack)
pre_save.connect(packArticle_pre_saved_receiver, sender=PackArticle)
post_save.connect(packArticle_post_delete_saved_receiver, sender=PackArticle)
post_delete.connect(packArticle_post_delete_saved_receiver, sender=PackArticle)


