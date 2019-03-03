from django.urls import path
from django.conf.urls import url

from .views import (
    EditGradesView, EditCredentialsView,
    AdminPageView
)


urlpatterns = [
    url(r'^$', AdminPageView.as_view(), name='admin'),
    url(r'^edit-grades/$', EditGradesView.as_view(), name='edit-grades'),
    url(r'^edit-credentials/$', EditCredentialsView.as_view(), name='edit-credentials')
    ]

