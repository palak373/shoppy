from django.urls import path, include

from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success', views.checkout_success, name='success')
]