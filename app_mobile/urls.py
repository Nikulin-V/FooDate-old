from django.urls import path

from app_mobile.views import HomeView, AppView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('app/', AppView.as_view(), name='app'),
]
