#from customization.models import Customized_product
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from users.models import GuestUsers
from users.models import NewUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class CartItem(models.Model):
	cart = models.ForeignKey("Cart",related_name="cartitems" , on_delete=models.CASCADE)
	limit = models.Q(app_label = 'products', model = 'pack') | models.Q(app_label = 'customization', model = 'custompack') | models.Q(app_label = 'products', model = 'product') 
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,limit_choices_to = limit)
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')
	quantity = models.PositiveIntegerField(default=1)
	total = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True)

	
	
	def set_itemType(self):
		self.content_type_label = self.content_type.name
		
	def __unicode__(self):
		return self.item.title

	def remove(self):
		return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if qty >= 1:
		
		price = instance.item.get_sale_price()
		print(price)
	
		total = Decimal(qty) * Decimal(price)
		
		instance.total = total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)



def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.set_itemType()
	

pre_save.connect(cart_item_post_save_receiver, sender=CartItem)

#post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
	active=models.BooleanField(default=True)
	user = models.ForeignKey(
		    settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True , blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	active = models.BooleanField(default=True)
	device_id = models.ForeignKey(GuestUsers, on_delete=models.CASCADE, blank=True,null=True)

	class Meta:
		unique_together=('user','device_id',)
	
	def __unicode__(self):
		return str(self.id)
	def update_subtotal(self):
		subtotal = 0
		items = self.cartitems.all()
		print(items)
		for item in items:
			subtotal += item.total
		
		self.subtotal = "%.2f" %(subtotal)
		self.save()
	def is_complete(self):
		self.active = False
		self.save()



def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)






@receiver(post_save, sender=GuestUsers)
def user_is_created(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(device_id=instance)