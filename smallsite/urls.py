from django.urls import path
from django.conf.urls import url

from .views import (
    SignUpView, LogInView,
    HomeView, ProfileView,
    GradesView,
    ProjectsView, NewsView,
    LogOutView
)


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/grades/$', GradesView.as_view(), name='grades'),
    url(r'^projects/$', ProjectsView.as_view(), name='projects'),
    url(r'^news/$', NewsView.as_view(), name='news'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    ]
