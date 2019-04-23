from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from smallsite.models import CustomUser, UserProfileInfo, Grades


class AddSubjectForm(forms.ModelForm):
    pass


class ChangeGradesForm(forms.ModelForm):
    subject = forms.CharField(max_length=255,
                              widget=forms.TextInput(attrs={"class": 'w3-input w3-border w3-round input-field'}))

    first_semester = forms.CharField(max_length=30,
                                     widget=forms.TextInput(attrs={"class": 'w3-input w3-border w3-round input-field'}))

    second_semester = forms.CharField(max_length=30,
                                      widget=forms.TextInput(attrs={"class": 'w3-input w3-border w3-round input-field'}))

    overall = forms.CharField(max_length=30,
                              widget=forms.TextInput(attrs={"class": 'w3-input w3-border w3-round input-field'}))

    class Meta:
        model = Grades
        fields = ('subject', 'first_semester', 'second_semester', 'overall')

    def save(self, commit=True):
        grades = super(ChangeGradesForm, self).save(commit=False)

        grades.subject = self.cleaned_data['subject']
        grades.first_semester = self.cleaned_data['first_semester']
        grades.second_semester = self.cleaned_data['second_semester']
        grades.overall = self.cleaned_data['overall']

        if commit:
            grades.save()

        return grades
