from django.urls import path
from django.conf.urls import url

from .views import (
    ShowGradesView, EditCredentialsView,
    AdminPageView, EditGradesView
)


urlpatterns = [
    url(r'^$', AdminPageView.as_view(), name='adminpage'),
    url(r'^show-grades/(?P<pk>\d+)/$', ShowGradesView.as_view(), name='show-grades'),
    url(r'^edit-credentials/(?P<pk>\d+)/$', EditCredentialsView.as_view(), name='edit-credentials'),
    url(r'^show-grades/(?P<pk>\d+)/edit-grades/(?P<subject_id>\d+)/$', EditGradesView.as_view(), name='edit-grades')
    ]

