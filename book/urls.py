from django.contrib.sitemaps.views import sitemap
from django.urls import path

from book.sitemaps import BookViewSitemap
from book.views import HomeView, ProductsView, RecipesView, ProductView, RecipeView
from core.views import robots_txt

sitemaps = {
    'book': BookViewSitemap
}

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<str:product_slug>', ProductView.as_view(), name='product'),
    path('recipes/', RecipesView.as_view(), name='recipes'),
    path('recipes/<str:recipe_slug>', RecipeView.as_view(), name='recipe'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

handler400 = 'app.error_views.bad_request'
handler403 = 'app.error_views.forbidden'
handler404 = 'app.error_views.not_found'
handler500 = 'app.error_views.internal_server_error'

