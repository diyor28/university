from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView
from smallsite.models import UserProfileInfo, CustomUser, Grades
from smallsite.forms import ProfileInfoChangeForm
from .forms import ChangeGradesForm
# Create your views here.


class AdminPageView(CreateView):
    template_name = 'admin/admin.html'

    def get(self, request, *args, **kwargs):
        context = {"students": CustomUser.objects.all()}
        return render(request, template_name=self.template_name, context=context)


class ShowGradesView(CreateView):
    template_name = 'admin/show_grades.html'
    form_class = ChangeGradesForm

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            user = CustomUser.objects.get(pk=pk)
        else:
            user = request.user

        grades = Grades.objects.filter(user=user)

        context = {"grades": grades,
                   "user": user}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            user = CustomUser.objects.get(pk=pk)
        else:
            user = request.user

        if 'add' in request.POST:
            subject = Grades(user=user)
            subject.save()
            return self.get(request)

        grades = Grades.objects.filter(user=user)

        context = {"grades": grades,
                   "user": user}
        return render(request, template_name=self.template_name, context=context)


class EditGradesView(CreateView):
    template_name = 'admin/edit_grades.html'
    form_class = ChangeGradesForm

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        subject_id = kwargs.get('subject_id')

        if pk:
            user = CustomUser.objects.get(pk=pk)
        else:
            user = request.user

        grades = Grades.objects.get(user=user, pk=subject_id)

        form = ChangeGradesForm(instance=grades)

        context = {"grades": grades,
                   "form": form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        subject_id = kwargs.get('subject_id')

        if pk:
            user = CustomUser.objects.get(pk=pk)
        else:
            user = request.user

        grades = Grades.objects.get(user=user, pk=subject_id)

        form = ChangeGradesForm(instance=grades, data=request.POST)

        saved = False

        if form.is_valid():
            form.save()
            saved = True

        context = {'grades': grades,
                   'form': form,
                   'saved': saved}
        return render(request, template_name=self.template_name, context=context)


class EditCredentialsView(CreateView):
    template_name = 'admin/edit_credentials.html'
    form_class = ProfileInfoChangeForm

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            user = CustomUser.objects.get(pk=pk)
        else:
            user = request.user

        form = self.form_class(initial={'first_name': user.userprofileinfo.first_name,
                                        'last_name': user.userprofileinfo.last_name,
                                        'profile_pic': user.userprofileinfo.profile_pic}, instance=user)
        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        if pk:
            user = CustomUser.objects.get(pk=pk)
        else:
            user = request.user

        form = self.form_class(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect(reverse("adminpage:adminpage"))

        context = {"form": form}
        return render(request, template_name=self.template_name, context=context)

