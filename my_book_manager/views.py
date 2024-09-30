import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomAuthUserCreationForm, CustomAuthUserLoginForm, UserDetailsForm


# Home view with search functionality
@login_required
def home_view(request):
    context = {}
    return render(request, 'book/home.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = CustomAuthUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomAuthUserCreationForm()
    return render(request, 'book/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomAuthUserLoginForm()
    return render(request, 'book/login.html', {'form': form})


@login_required
def change_user_details(request):
    user = request.user
    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserDetailsForm(instance=user)

    return render(request, 'book/change_user_details.html', {'form': form})
