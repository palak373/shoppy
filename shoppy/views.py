from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from carts.models import Cart
from products.models import Product

from .forms import ContactForm

def home(request):
    featured_products = Product.objects.featured()
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    context = {
        'featured_products':featured_products,
        'cart': cart_obj,
    }
    return render(request, 'index.html', context)


def contact(request):
    contact_form = ContactForm(request.POST or None)
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({'message': 'Thanks For Your Feedback.'})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        return HttpResponse(errors, status=400, content_type='application/json')
    context = {
        'form': contact_form
    }
    return render(request, 'contact.html', context)