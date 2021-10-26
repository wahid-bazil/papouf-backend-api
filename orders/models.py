from decimal import Decimal

from django.db.models.deletion import SET_NULL
from shipping.models import ShippingMode
#from delivery.models import Delivery_Mode
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from cart.models import Cart
from accounts.models import NewUser,Address

from django.utils.timezone import datetime

from .mixins import send_order_email



ORDER_STATUS_CHOICES = (
	('created', 'Préparation pour la livraison'),
	('shipping', 'En cours de livraison'),
	('shipped', 'Livrée'),
	('refunded', 'Retournéé'),

)

class OrderEmail(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    subject = models.CharField(max_length=30)
    text =models.TextField(_('subject'), max_length=500, blank=True)
    

class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    created=models.DateTimeField(default=datetime.now(timezone.utc))
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE ,null=True, blank=True)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE ,null=True, blank=True)
    shipping_mode = models.ForeignKey(ShippingMode,on_delete=models.CASCADE,null=True, blank=True)
    shipping_address = models.ForeignKey(Address,on_delete=models.CASCADE, related_name='shipping_address' ,blank=True ,null=True)
    shipping_total_price = models.FloatField(null=True, blank=True)
    shipping_time = models.IntegerField(null=True, blank=True)
    order_total = models.FloatField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    #payment_mode = models.ForeignKey(PaymentMode,on_delete=SET_NULL,null=True, blank=True)
    class Meta:
        ordering = ['-id']


"""

def Order_prost_save_receiver(sender, created, instance, *args, **kwargs):
    if created:
        ctx = {
        'order': instance,
        'msg':  OrderEmail.objects.get(status='created')
        }
        

post_save.connect(Order_prost_save_receiver, sender=Order)


def Order_pre_save_receiver(sender, instance, *args, **kwargs):

    try :
        pre_save_instance = Order.objects.get(pk=instance.pk)
        if pre_save_instance.status == 'created' and instance.status == 'shipping':
            ctx = {
            'order': instance,
            'msg':  OrderEmail.objects.get(status='shipping')
            }
            send_order_email(ctx , instance.user.email)
        elif pre_save_instance.status == 'shipping' and instance.status == 'shipped':
            ctx = {
            'order': instance,
            'msg':  OrderEmail.objects.get(status='shipped')
            }
            send_order_email(ctx , instance.user.email)
        elif pre_save_instance.status == 'shipped' and instance.status == 'refunded':
            ctx = {
            'order': instance,
            'msg':  OrderEmail.objects.get(status='refunded')
            }
            send_order_email(ctx , instance.user.email)
    except:
        pass
pre_save.connect(Order_pre_save_receiver, sender=Order)
"""