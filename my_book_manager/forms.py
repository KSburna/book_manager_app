from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomAuthUser
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomAuthUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class CustomAuthUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }