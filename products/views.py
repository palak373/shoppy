from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from .models import Product
# Create your views here.

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        print(cart_obj.products.all())
        return context

class ProductDetailView(ObjectViewedMixin, generic.DetailView):
    model = Product
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        print(slug)
        instance = get_object_or_404(Product, slug=slug)
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance


            


class ProductFeaturedListView(generic.ListView):
    model = Product
    template_name = 'products/f_index.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured() 

    
class ProductFeaturedDetailView(ObjectViewedMixin, generic.DetailView):    
    queryset = Product.objects.featured()
    model = Product
    template_name = 'products/f_detail.html'