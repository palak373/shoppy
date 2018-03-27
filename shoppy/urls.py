"""shoppy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include

from addresses.views import checkout_address_view, checkout_address_reuse_view
from carts.views import cart_home_api_view

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    # my apps
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),     
    path('cart/', include('carts.urls', namespace='carts')),
    path('billing/', include('billing.urls', namespace='billing')),    
    path('checkout/address/create/', checkout_address_view, name='checkout_address_view'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),

    # API-AJAX
    path('api/cart/', cart_home_api_view, name='cart_api_view'),   

    # thrid-parites
    path('avatar/', include('avatar.urls')),               
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)