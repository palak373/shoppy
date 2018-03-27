import math

from django.db import models
from django.db.models.signals import pre_save, post_save

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart

from .utils import unique_order_id_generator
# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        order_qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if order_qs.count() == 1:
            created = False
            order_obj = order_qs.first()
        else:
            order_obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return order_obj, created

class Order(models.Model):
    order_id            = models.CharField(max_length=120, blank=True)
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    shipping_address    = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    billing_address     = models.ForeignKey(Address,related_name='billing_address', on_delete=models.CASCADE, blank=True, null=True)
    cart                = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status              = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total      = models.DecimalField(default=400.00, max_digits=20, decimal_places=2)
    total               = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    active              = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        f_total = format(new_total, '.2f')
        self.total = new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

def order_pre_save(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(order_pre_save, sender=Order)

def cart_post_save(sender, instance, created, *args, **kwargs):
    if not created:
        qs = Order.objects.filter(cart__id=instance.id)
        if qs.count() == 1:
            order = qs.first()
            order.update_total()

post_save.connect(cart_post_save, sender=Cart)

def order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(order_post_save, sender=Order)