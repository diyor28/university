from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from .models import CustomUser, UserProfileInfo, Grades


class LogInForm(forms.Form):
    email = forms.EmailField(label='Email:')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True) -> CustomUser:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = True
        if commit:
            user.save()
        return user


class UserProfileInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfileInfo
        fields = ('first_name', 'last_name', 'profile_pic')


class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'w3-input w3-border w3-round',
                                                                 "placeholder": 'Password'}))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'w3-input w3-border w3-round',
                                                                      "placeholder": 'New password...'}))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'w3-input w3-border w3-round',
                                                                      "placeholder": 'New password...'}))

    class Meta:
        model = CustomUser
        fields = ('password', )

    def clean(self):
        password = self.cleaned_data.get('password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if not self.instance.check_password(password):
            raise forms.ValidationError('Password is incorrect')

        if not new_password1 == new_password2:
            raise forms.ValidationError('Passwords do not match')

        if self.instance.check_password(new_password2):
            raise forms.ValidationError('New password can not be the same as old')

        return self.cleaned_data

    def save(self, commit=True):
        user = super(ResetPasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('new_password1'))
        if commit:
            user.save()
        return user


class ProfileInfoChangeForm(forms.ModelForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'w3-input w3-border w3-round'
                                                            }))

    first_name = forms.CharField(label='First name',
                                 widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'
                                                               }))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'
                                                              }))

    profile_pic = forms.ImageField(label='Choose File', required=True,
                                   widget=forms.FileInput(attrs={'class': 'image-field'}))

    class Meta:
        model = UserProfileInfo
        fields = ('email', 'first_name', 'last_name', 'profile_pic')

    def save(self, commit=True):
        user = super(ProfileInfoChangeForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.userprofileinfo.first_name = self.cleaned_data['first_name']
        user.userprofileinfo.last_name = self.cleaned_data['last_name']
        user.userprofileinfo.profile_pic = self.files['profile_pic']

        if commit:
            user.save()
            user.userprofileinfo.save()

        return user


class EditGradesForm(forms.ModelForm):
    pass


class CustomUserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with adminpage's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

