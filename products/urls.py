from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('featured/', views.ProductFeaturedListView.as_view(), name='f_index'),
    path('featured/<slug:slug>/', views.ProductFeaturedDetailView.as_view(), name='f_detail'), 
    path('', views.ProductListView.as_view(), name='index'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),  
]