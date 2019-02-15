from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import CustomUserCreationForm, LogInForm, UserProfileInfoForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'accounts/signup.html'
    registered = False

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
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            self.registered = True

            email = user_form.cleaned_data.get("email")
            password = user_form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('/smallsite/profile/')

        return render(request, template_name=self.template_name, context={"form": user_form})


class LogInView(CreateView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy("/smallsite/")
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
            login(request, user)
            return redirect('/smallsite/profile')
        return render(request, template_name=self.template_name, context={'form': form})


class HomeView(TemplateView):
    template_name = 'accounts/home.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, template_name=self.template_name)


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        return render(request, template_name=self.template_name, context={"first_name": first_name,
                                                                          "last_name": last_name,
                                                                          "email": email})


class GradesView(CreateView):
    template_name = 'accounts/grades.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


class StudentsInfoView(CreateView):
    template_name = 'accounts/students.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


class AboutUsView(CreateView):
    template_name = 'accounts/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})

