from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import SignUpForm, LogInForm, UserProfileInfoForm
from .models import UserProfileInfo


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    registered = False

    def form_valid(self, form):
        valid = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=password)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return valid

    def get(self, request, *args, **kwargs):
        user_form = self.form_class(initial=self.initial)
        profile_form = UserProfileInfoForm(initial=self.initial)

        return render(request, template_name=self.template_name, context={'user_form': user_form,
                                                                          'profile_form': profile_form,
                                                                          'registered': self.registered})

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            self.registered = True

            email = user_form.cleaned_data.get("email")
            password = user_form.cleaned_data.get("password1")

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/smallsite/profile/')

        return render(request, template_name=self.template_name, context={"user_form": user_form,
                                                                          "profile_form": profile_form})


class LogInView(CreateView):
    template_name = 'accounts/login.html'
    form_class = LogInForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=raw_password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('/smallsite/profile')
        return render(request, template_name=self.template_name, context={'form': form})


class HomeView(CreateView):
    template_name = 'accounts/home.html'
    form_class = LogInForm

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=raw_password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('/smallsite/profile')
        return render(request, template_name=self.template_name, context={'form': form})


class ProfileView(CreateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        email = request.user.email
        query = UserProfileInfo.objects.all().filter(user=request.user)[0]
        print(query)
        first_name = query.first_name
        last_name = query.last_name
        return render(request, template_name=self.template_name, context={"email": email,
                                                                          "first_name": first_name,
                                                                          "last_name": last_name})


class GradesView(CreateView):
    template_name = 'accounts/grades.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


class ProjectsView(CreateView):
    template_name = 'accounts/projects.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


class NewsView(CreateView):
    template_name = 'accounts/news.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


class LogOutView(CreateView):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, template_name=self.template_name, context={})

