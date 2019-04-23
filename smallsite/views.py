from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import UserProfileInfo, Grades

from .forms import (
    SignUpForm, LogInForm,
    UserProfileInfoForm, ProfileInfoChangeForm,
    ResetPasswordForm)


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

        contex = {"user_form": user_form,
                  "profile_form": profile_form,
                  "registered": self.registered}

        return render(request, template_name=self.template_name, context=contex)

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        grades = Grades()

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            grades.user = user
            grades.save()

            self.registered = True

            email = user_form.cleaned_data.get("email")
            password = user_form.cleaned_data.get("password1")

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect(reverse('profile'))

        context = {"user_form": user_form,
                   "profile_form": profile_form}
        return render(request, template_name=self.template_name, context=context)


class LogInView(CreateView):
    template_name = 'accounts/login.html'
    form_class = LogInForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=raw_password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect(reverse("profile"))

        context = {'form': form}
        return render(request, template_name=self.template_name, context=context)


class LogOutView(CreateView):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        context = {}
        return render(request, template_name=self.template_name, context=context)


class GradesView(CreateView):
    template_name = 'accounts/grades.html'

    def get(self, request, *args, **kwargs):
        context = {"grades": Grades.objects.filter(user=request.user)}
        return render(request, template_name=self.template_name, context=context)


class ProfileView(CreateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)


class ProfileInfoChangeView(CreateView):
    template_name = 'accounts/edit_profile.html'
    form_class = ProfileInfoChangeForm

    def get(self, request, *args, **kwargs):

        form = self.form_class(initial={'first_name': request.user.userprofileinfo.first_name,
                                        'last_name': request.user.userprofileinfo.last_name,
                                        }, instance=request.user)
        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("smallsite:profile"))

        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)


class ResetPasswordView(CreateView):
    template_name = 'accounts/reset_password.html'
    form_class = ResetPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("profile"))

        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)


