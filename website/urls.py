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
