from decimal import Decimal
#from delivery.models import Delivery_Mode


from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from cart.models import Cart
from users.models import NewUser,Address



""""
class UserCheckout(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True) #not required
	email = models.EmailField(unique=True)
	#braintree_id = models.CharField(max_length=120, null=True, blank=True)

"""

"""
@property
	def get_braintree_id(self,):
		instance = self
		if not instance.braintree_id:
			result = braintree.Customer.create({
			    "email": instance.email,
			})
			if result.is_success:
				instance.braintree_id = result.customer.id
				instance.save()
		return instance.braintree_id
	def get_client_token(self):
		customer_id = self.get_braintree_id
		if customer_id:
			client_token = braintree.ClientToken.generate({
			    "customer_id": customer_id
			})
			return client_token
		return None
"""

def update_braintree_id(sender, instance, *args, **kwargs):
	if not instance.braintree_id:
		instance.get_braintree_id


#post_save.connect(update_braintree_id, sender=UserCheckout)




ORDER_STATUS_CHOICES = (
	('created', 'Created'),
	('shipping', 'Shipping'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded'),
)


class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    created=models.DateTimeField(default=timezone.now)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE)
    #delivery_mode = models.ForeignKey(Delivery_Mode,on_delete=models.CASCADE,null=True)
    shipping_address = models.ForeignKey(Address,on_delete=models.CASCADE, related_name='shipping_address' ,blank=True ,null=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99,blank=True)
    order_total = models.DecimalField(max_digits=50, decimal_places=2, blank=True)
    is_paid = models.BooleanField(default=False)
    #payment_mode = models.ForeignKey(Payment_Mode,on_delete=models.CASCADE,null=True)

	

    """def __unicode__(self):
	    return "Order_id: %s, Cart_id: %s"%(self.id, self.cart.id)"""

    class Meta:
        ordering = ['-id']

""" 
    def get_absolute_url(self):
		return reverse("order_detail", kwargs={"pk": self.pk})
	def mark_completed(self, order_id=None):
		self.status = "paid"
		if order_id and not self.order_id:
			self.order_id = order_id
		self.save()
	@property
	def is_complete(self):
		if self.status == "paid":
			return True
		return False
"""

def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.delivery_mode.shipping_total_price
    instance.shipping_total_price = shipping_total_price
    cart_total = instance.cart.subtotal
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total
    

pre_save.connect(order_pre_save, sender=Order)

# #if status == "refunded":
# 	braintree refud
# post_save.connect()


def order_is_created(sender,instance,created,**kwargs):
    if created:
       instance.cart.is_complete()
       Cart.objects.create(user=instance.user)
post_save.connect(order_is_created,sender=Order)