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
    path('django-adminpage/', admin.site.urls, name='django-adminpage'),
    path('adminpage/', include(('adminpage.urls', 'adminpage'), namespace='adminpage')),
    path('smallsite/', include(('smallsite.urls', 'smallsite'), namespace='smallsite')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^news/$', NewsView.as_view(), name='news'),
    url(r'^projects/$', ProjectsView.as_view(), name='projects')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
