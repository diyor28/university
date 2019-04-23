from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token


from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from .models import UserProfileInfo, Grades, CustomUser

from .forms import (
    SignUpForm, LogInForm,
    UserProfileInfoForm, ProfileInfoChangeForm,
    ResetPasswordForm)


def activate(request, uidb64, token):
    print('activate function called')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        print('Successfully activated')
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'smallsite/signup.html'

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
                  "profile_form": profile_form}

        return render(request, template_name=self.template_name, context=contex)

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        grades = Grades()

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            user.active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            grades.user = user
            grades.save()

            email_adress = user_form.cleaned_data.get("email")

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('smallsite/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email_adress
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, template_name='smallsite/confirm_email.html')

        context = {"user_form": user_form,
                   "profile_form": profile_form}
        return render(request, template_name=self.template_name, context=context)


class LogInView(CreateView):
    template_name = 'smallsite/login.html'
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
            return redirect(reverse("smallsite:profile"))

        context = {'form': form}
        return render(request, template_name=self.template_name, context=context)


class LogOutView(CreateView):
    template_name = 'smallsite/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        context = {}
        return render(request, template_name=self.template_name, context=context)


class GradesView(CreateView):
    template_name = 'smallsite/grades.html'

    def get(self, request, *args, **kwargs):
        context = {"grades": Grades.objects.filter(user=request.user)}
        return render(request, template_name=self.template_name, context=context)


class ProfileView(CreateView):
    template_name = 'smallsite/profile.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)


class ProfileInfoChangeView(CreateView):
    template_name = 'smallsite/edit_profile.html'
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
    template_name = 'smallsite/reset_password.html'
    form_class = ResetPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("smallsite:profile"))

        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)


