from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.views import HomeView, AppView
from foodate import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('app/', AppView.as_view(), name='app'),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include('users.urls'), name='auth'),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls'))
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
