from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from accounts.models import GuestProfile
from billing.models import BillingProfile
from products.models import Product
from orders.models import Order

from .models import Cart

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_w8E9YC55rUXiwjqsBuqb6Uka")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_Oj1c4taJkjHrJOkIrGz8sviW")

stripe.api_key = STRIPE_SECRET_KEY


def cart_home_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [
        {   
            'id': p.id,
            'url':p.get_absolute_url(),
            'title': p.title, 
            'price': p.price
        }
         for p in cart_obj.products.all()]
    data = {
        'products': products,
        'subtotal': cart_obj.subtotal,
        'total':cart_obj.total
    }
    return JsonResponse(data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context={
        'cart_obj':cart_obj
    }
    return render(request, 'carts/home.html', context)

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    product_obj = get_object_or_404(Product,id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
        added = False
    else:
        cart_obj.products.add(product_obj)
        added = True
    request.session['cart_items'] = cart_obj.products.count()

    if request.is_ajax():
        print(request)
        print('roses are red violets are blueunexpected "{"on line 32')
        data = {
            'added': added,
            'removed': not added,
            'cartItemCount': cart_obj.products.count()
        }
        return JsonResponse(data)
        # return JsonResponse({'message': 'err'}, status=400)
    return redirect('carts:home')

def checkout(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count() == 0:
        return redirect('carts:home')

    login_form = LoginForm(request.POST or None)
    guest_form = GuestForm(request.POST or None)
    shipping_address_form = AddressForm()
    billing_address_form = AddressForm()

    shipping_address_id = request.session.get('shipping_address_id', None)    
    billing_address_id = request.session.get('billing_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    order_obj = None
    address_qs = None
    has_cards = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id) 
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_cards = billing_profile.has_cards
        
    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            is_charged, message = billing_profile.charge(order_obj)
            if is_charged:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()

                return redirect('carts:success')
            else:
                print(message)
                return redirect('carts:checkout')

    context={
        'cart_obj':cart_obj,
        'billing_profile':billing_profile,
        'object':order_obj,
        'login_form':login_form,
        'guest_form': guest_form,
        'shipping_address_form':shipping_address_form,
        'billing_address_form':billing_address_form,
        'address_qs': address_qs,
        'has_cards':has_cards,
        'publish_key': STRIPE_PUB_KEY,
    }
    return render(request, 'carts/checkout.html', context)
    

def checkout_success(request):
    return render(request, 'carts/success.html', {})