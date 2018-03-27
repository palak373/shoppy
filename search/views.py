from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from products.models import Product
# Create your views here.

class SearchProductListView(generic.ListView):
    template_name = 'search/view.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        q = request.GET.get('q')
        if q is not None:
            return Product.objects.search(q)     
        return Product.objects.none() 