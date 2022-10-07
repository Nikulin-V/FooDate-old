from django.contrib.sitemaps.views import sitemap
from django.urls import path

from app_mobile.sitemaps import AppViewSitemap, HomeViewSitemap
from app_mobile.views import HomeView, AppView, PrivacyPolicyView
from core.views import robots_txt

sitemaps = {
    'home': HomeViewSitemap,
    'app': AppViewSitemap
}

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('app/', AppView.as_view(), name='app'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

handler400 = 'app.error_views.bad_request'
handler403 = 'app.error_views.forbidden'
handler404 = 'app.error_views.not_found'
handler500 = 'app.error_views.internal_server_error'
