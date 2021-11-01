
from cart.models import *

class UserNumbers:
    def get_current_cartitems (self ,user):
        cart=Cart.objects.get(user=user , active=True)
        return len(cart.cartitems.all())
    def get_orders_made(self ,email):
        return 3
    def get_orders_in_process(self ,email):
        return 3
    def get_orders_refunded(self ,email):
        return 3

    


