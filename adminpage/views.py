from django.shortcuts import render
from django.views.generic import CreateView
from smallsite.models import UserProfileInfo, CustomUser
# Create your views here.


class AdminPageView(CreateView):
    template_name = 'admin/admin.html'

    def get(self, request, *args, **kwargs):
        context = {"students": CustomUser.objects.all()}
        return render(request, template_name=self.template_name, context=context)


class EditGradesView(CreateView):
    template_name = 'admin/edit_grades.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)


class EditCredentialsView(CreateView):
    template_name = 'admin/edit_grades.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)


