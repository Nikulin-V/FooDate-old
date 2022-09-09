from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class BookViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return ['products', 'recipes']

    def location(self, item):
        return reverse(item)
