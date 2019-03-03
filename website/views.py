from django.views.generic import CreateView

from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login

from smallsite.forms import LogInForm


class HomeView(CreateView):
    template_name = 'general/home.html'
    form_class = LogInForm

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=raw_password)
            if user is None:
                return render(request, template_name=self.template_name,
                              context={"form": form,
                                       "error_message": "Password or email entered are incorrect"})

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect(reverse("smallsite:profile"))

        context = {'form': form}
        return render(request, template_name=self.template_name, context=context)


class ProjectsView(CreateView):
    template_name = 'general/projects.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)


class NewsView(CreateView):
    template_name = 'general/news.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)
