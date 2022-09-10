from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class AppViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return ['app']

    def location(self, item):
        return reverse(item)
