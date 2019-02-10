from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import login, authenticate
# from .models import UserProfile
from .models import User
from .forms import SignUpForm, LogInform
from . hash_utils import hash_password

# Create your views here.


def home(request):
    return render(request, template_name='accounts/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = hash_password(form.cleaned_data.get("password"))
            user.password = password
            user.save()
            return redirect('/smallsite/profile/')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LogInform(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_password = form.cleaned_data.get("password")

            # query = UserProfile.objects.all().filter(email=email)
            query = User.objects.all().filter(email=email)
            if query:
                db_password = query[0].password
                first_name = query[0].first_name
                last_name = query[0].last_name
                if hash_password(user_password) == db_password:
                    return HttpResponse(f"Welcome {first_name} {last_name}")
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': True})
    else:
        form = LogInform()

    return render(request, 'accounts/login.html', {'form': form, 'error': False})


def profile(request):
    return render(request, 'accounts/profile.html')
