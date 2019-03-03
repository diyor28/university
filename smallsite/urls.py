from django.urls import path
from django.conf.urls import url

from .views import (
    SignUpView, ResetPasswordView,
    ProfileView, GradesView,
    LogOutView, ProfileInfoChangeView,
)


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/grades/$', GradesView.as_view(), name='grades'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^profile/edit/$', ProfileInfoChangeView.as_view(), name='edit-profile'),
    url(r'^profile/upload/$', SignUpView.as_view(), name='upload-picture'),
    url(r'^profile/reset-password/$', ResetPasswordView.as_view(), name='reset-password'),
    ]

