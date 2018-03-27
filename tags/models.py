from django.db import models
from django.db.models.signals import pre_save

from products.models import Product

from .utils import unique_slug_generator

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title

def tag_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# Signals
pre_save.connect(tag_pre_save, sender=Tag)