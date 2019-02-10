from django import forms
# from django.contrib.auth.forms import User
# from . models import UserProfile
from .models import User


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')


class LogInform(forms.Form):
    email = forms.CharField(label='Email:', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())


