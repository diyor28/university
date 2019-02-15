from django.urls import path
from django.conf.urls import url

from .views import (
    SignUpView, LogInView,
    HomeView, ProfileView,
    StudentsInfoView, GradesView,
    AboutUsView
)


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^studinfo/$', StudentsInfoView.as_view(), name='students'),
    url(r'^profile/grades/$', GradesView.as_view(), name='grades'),
    url(r'^about/$', AboutUsView.as_view(), name='aboutus'),
    url(r'^$', HomeView.as_view(), name='home'),
    ]
