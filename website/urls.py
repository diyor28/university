
"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf.urls import url
from . views import (
    HomeView, NewsView,
    ProjectsView
)

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('django-admin/', admin.site.urls, name='django-admin'),
    path('admin/', include(('adminpage.urls', 'adminpage'), namespace='adminpage')),
    path('accounts/', include(('smallsite.urls', 'smallsite'), namespace='smallsite')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^news/$', NewsView.as_view(), name='news'),
    url(r'^projects/$', ProjectsView.as_view(), name='projects')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
