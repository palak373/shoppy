from django.urls import path

from .views import SignupView, LoginView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts_index, name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit', views.profile_edit, name='edit'),
    path('delete/', views.delete_view, name='delete'),
    path('register/guest', views.guest_regiter_view, name='guest_register'),    
]