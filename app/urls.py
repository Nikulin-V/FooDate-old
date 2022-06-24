from django.contrib import admin
from django.urls import path, include

from app.views import HomeView, AppView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('app/', AppView.as_view(), name='app'),
    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include('users.urls'), name='auth')
]
