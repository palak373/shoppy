from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import BillingProfile, Card

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_w8E9YC55rUXiwjqsBuqb6Uka")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_Oj1c4taJkjHrJOkIrGz8sviW")

stripe.api_key = STRIPE_SECRET_KEY

def payment_method(request):

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('carts:home')

    next_ = request.GET.get('next')
    next_url = next_
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    context = {
        'publish_key': STRIPE_PUB_KEY,
        'next_url': next_url
    }
    return render(request, 'billing/payment.html', context)

def payment_create_method(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message':'Cannot found User'}, status_code=401)

        token = request.POST.get('token')
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id)
            # card_response = customer.sources.create(source=token)

            new_card_obj = Card.objects.add_new(billing_profile, token)
            
            print(new_card_obj)
        return JsonResponse({'message': 'done'})

    return HttpResponse('error', status_code=401)