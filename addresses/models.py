from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),    
)

class AddressManager(models.Manager):
    pass

class Address(models.Model):
    billing_profile  = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, blank=True, null=True)
    city            = models.CharField(max_length=120)
    state           = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='India')
    zip_code        = models.CharField(max_length=120)

    objects = AddressManager()
    
    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        s = self
        return '{l1}, \n{l2}, \n{city}, \n{st}-{zp}, \n{country}'.format(l1=s.address_line_1, l2=s.address_line_2 or "", city=s.city, st=s.state, zp=s.zip_code, country=s.country)