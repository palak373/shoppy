from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .forms import SignupForm, LoginForm, ProfileEditForm, GuestForm
from .models import UserProfile, GuestProfile
from .signals import user_logged_in


# Create your views here.
def accounts_index(request):
    context = {}
    return render(request, 'accounts/index.html', context)

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        else:
            form = self.form_class() 
            return render(request, self.template_name, {'form': form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        else:
            form = self.form_class() 
            return render(request, self.template_name, {'form': form})

    
    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data["email"]
        next = request.POST.get('next')
        # first_name = form.cleaned_data("first_name")
        # last_name = form.cleaned_data("last_name")
        password = form.cleaned_data["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_user_id']
            except:
                pass
            if next:
                return redirect(next)
            return redirect('home')
        return super(LoginView, self).form_invalid(form)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required(login_url="/accounts/login/")
def profile_view(request):
    user = request.user
    tab = request.GET.get('tab')
    
    context = {
        'user':user,
        'tab':tab
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url="/accounts/login/")
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        # print(form.errors)
        if form.is_valid():
            user.bio = request.POST['bio']
            print(form.errors)
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'accounts/profile_edit.html', {'user':user, 'form':form})

# def users_view(request):
#     user = request.user
#     users = UserProfile.objects.all().exclude(email=user.email)
#     context = {
#         'user':user,
#         'users':users
#     }
#     return render(request, 'accounts/all_users.html', context)

@login_required(login_url="/accounts/login/")
def delete_view(request):
    user = request.user
    
    if request.method == 'POST':
        user.delete()
        messages.add_message(request, messages.SUCCESS, 'Account Deleted')
        return redirect('accounts:signup')
    context = {}
    return render(request, 'accounts/delete.html', context)


############  GUEST_USER   ##############

def guest_regiter_view(request):
    form = GuestForm(request.POST or None)
    _next = request.GET.get('next')
    _next_post = request.POST.get('next')
    _next_url = _next or _next_post or None

    if form.is_valid():
        email = form.cleaned_data.get('email')
        guest_user = GuestProfile.objects.create(email=email)
        request.session['guest_user_id'] = guest_user.id
        if is_safe_url(_next_url, request.get_host()):
            return redirect(_next_url)
        else:
            return redirect('accounts:signup')
    return redirect('accounts:signup')