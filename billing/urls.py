from django.urls import path

from . import views

app_name = 'billing'

urlpatterns = [
    path('payment-method/', views.payment_method, name='payment_method'),
    path('payment-method/create/', views.payment_create_method, name='payment_create_method'),      
]