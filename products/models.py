from cart.models import CartItem
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from providers.models import Provider
#from category.models import   PackType
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _



def upload_to(instance, filename):
    print(instance._meta.verbose_name == "productimage")
    return 'posts/{filename}'.format(filename=filename)



class ItemStatus(models.Model):
	title = models.CharField(max_length=50 ,primary_key=True)

class test (models.Model):
	name = models.CharField(max_length=30)
	#boxe = models.ForeignKey('Boxe', on_delete=models.CASCADE, null=True)



class Product (models.Model):
    status = models.ForeignKey(ItemStatus,on_delete=models.SET_NULL ,null=True ,blank=True)
    title=models.CharField(max_length=35)
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
    #category = models.ManyToManyField("category.ProductCategory" ,related_name='items' ,blank=True)
    #test_category = models.ForeignKey(Category,on_delete=models.CASCADE ,null=True , blank=True ,related_name='itemsTest')
    promo = models.BooleanField(default=False)



    class Meta :
        verbose_name = 'product'
  
    def get_sale_price(self):
      return self.sale_price
    def get_cost_price (self):
      return self.cost_price	


class Pack(models.Model):
	status = models.ForeignKey(ItemStatus,on_delete=models.SET_NULL ,null=True ,blank=True)
	title = models.CharField(max_length=120)
	cost_price = models.DecimalField(decimal_places=2, max_digits=20,default=0)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, default=0,)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(default=1)
	items = models.ManyToManyField("Article",through='PackArticle')
	boxe = models.ForeignKey("Boxe",on_delete=CASCADE,null=True,blank=True)#optional field for small packs
	is_customized = models.BooleanField(default=False)
	created=models.DateTimeField(default=timezone.now)
	description = models.CharField(max_length=30,default="")
	cartItem = GenericRelation(CartItem,related_query_name='item_pack')
	#category =  models.ForeignKey(PackCategory,on_delete=CASCADE, null=True,related_name='items')
	#pack_type = models.ForeignKey(PackType , on_delete=CASCADE, blank=True , null=True)

	class Meta :
		verbose_name = 'pack'


	def update_nb_items(self):
		nb=self.items.all().count()
		self.nb_items=nb
		self.save()
	def get_sale_price(self):
		return self.sale_price
	def get_cost_price (self):
		return self.cost_price	




# """""""""""""""""""""""""""""""""""""""Pack Components"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Boxe (models.Model):
	title = models.CharField(max_length=30)
	cost_price = models.IntegerField()
	sale_price =  models.IntegerField()
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True)
	created=models.DateTimeField(default=timezone.now)
	provider = models.ForeignKey(Provider,on_delete=models.CASCADE,blank=True, null=True)
	description = models.CharField(max_length=150,default="")
	space = models.IntegerField(null=False)

	class Meta :
		verbose_name = 'boxe'
	

	def get_sale_price(self):
		return self.sale_price
	def get_cost_price (self):
		return self.cost_price	
	
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
	def get_children(self) :
		all_children = []
		#print(self.child.all())
		for first_child in self.child.all():
			all_children.append(first_child)
			all_children.extend(first_child.get_children())
		return all_children

	class Meta :
		verbose_name = 'article'
		ordering = ['sale_price']

		


	def get_sale_price(self):
		return self.sale_price
	def get_cost_price (self):
		return self.cost_price
			



class PackArticle(models.Model):
	pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
	item = models.ForeignKey(Article,on_delete=CASCADE)
	quantity = models.IntegerField(default=1)
	total = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)

	def update_total(self):
		total=self.item.sale_price*self.quantity
		self.total=total


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	product = instance
	variations = product.variation_set.all()
	if variations.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.prix = product.prix
		new_var.save()



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
pre_save.connect(product_presaved_receiver, sender=Product)
pre_save.connect(packArticle_pre_saved_receiver, sender=PackArticle)
post_save.connect(packArticle_post_delete_saved_receiver, sender=PackArticle)
post_delete.connect(packArticle_post_delete_saved_receiver, sender=PackArticle)


