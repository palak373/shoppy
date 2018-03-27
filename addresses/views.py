from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile

from .forms import AddressForm
from .models import Address

def checkout_address_view(request):
    form = AddressForm(request.POST or None)
    _next = request.GET.get('next')
    _next_post = request.POST.get('next')
    _next_url = _next or _next_post or None
    if form.is_valid():
        # print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            # print(billing_profile)
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()

            request.session[address_type + "_address_id"] = instance.id
            # print(address_type + "_address_id")

        else:
            return redirect('carts:home')
        if is_safe_url(_next_url, request.get_host()):
            return redirect(_next_url)
    return redirect('carts:home')

def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        _next = request.GET.get('next')
        _next_post = request.POST.get('next')
        _next_url = _next or _next_post or None

        if request.method == 'POST':
            print(request.POST)
            address_type = request.POST.get('address_type', 'shipping')
            instance_id = request.POST.get('shipping_address', None)       
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if instance_id is not None:
                address_qs = Address.objects.filter(billing_profile=billing_profile, id=instance_id)
                if address_qs.exists():
                    request.session[address_type + "_address_id"] = instance_id

                if is_safe_url(_next_url, request.get_host()):
                    return redirect(_next_url)
    return redirect('carts:home')
        