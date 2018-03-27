import os
import random

from django.urls import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save

from .utils import rand_uid, rand_slug

# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.split(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1000000, 99999999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    

    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, q):
        return self.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(price__icontains=q)|Q(tag__title__icontains=q)).distinct()

    

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def featured(self):
        return self.get_queryset().filter(featured=True)
        
    def search(self, q):
        return self.get_queryset().search(q)

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    slug = models.SlugField(max_length=8, unique=True)
    image = models.ImageField(upload_to=upload_image_path)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


def create_slug(product, new_slug=None):
    slug = rand_slug()
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = '{slug}{id}'.format(slug=slug, id=product.id)
        return create_slug(product, new_slug=new_slug)
    return slug

def product_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

# Signals
pre_save.connect(product_pre_save, sender=Product)