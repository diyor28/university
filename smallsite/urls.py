from django.urls import path
from django.conf.urls import url, include

from .views import (
    SignUpView, ResetPasswordView,
    ProfileView, GradesView,
    LogOutView, ProfileInfoChangeView,
    activate
)


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/grades/$', GradesView.as_view(), name='grades'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^profile/edit/$', ProfileInfoChangeView.as_view(), name='edit-profile'),
    url(r'^profile/upload/$', SignUpView.as_view(), name='upload-picture'),
    url(r'^profile/reset-password/$', ResetPasswordView.as_view(), name='reset-password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    ]

