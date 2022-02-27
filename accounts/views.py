from audioop import reverse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def register_view(request):
    form = RegisterForm(request.POST)

    if form.is_valid():
        u_name = form.cleaned_data.get('username')
        f_name = form.cleaned_data.get('first_name')
        l_name = form.cleaned_data.get('last_name')
        e_mail = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = User.objects.create_user(username=u_name, first_name=f_name, last_name=l_name, email=e_mail, password=password)

        if user:
            messages.add_message(request, messages.INFO, f'{u_name} Account Created Successfully.')
        form = RegisterForm()
        return redirect(reverse('accounts:register'))

    
    data = {'form': form}

    return render(request, 'accounts/pages/register.html', data)

def login_view(request):
    form = LoginForm(request.POST)

    if form.is_valid():
       u_name = form.cleaned_data.get('username')
       password = form.cleaned_data.get('password')

       user = authenticate(username=u_name, password=password)

       if user is not None:
           login(request, user)
           return redirect(reverse('myexpense:dashboard'))

       else:
            messages.add_message(request, messages.INFO, 'Invalid Username or Password.')
    

    data = {'form': form}
    return render(request, 'accounts/pages/login.html', data)

def logout_view(request):
    logout(request)

    return redirect(reverse('accounts:login'))

    

