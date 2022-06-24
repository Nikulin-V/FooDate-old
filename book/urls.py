from django.urls import path

from book.views import HomeView, ProductsView, RecipesView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='products'),
    path('recipes/', RecipesView.as_view(), name='recipes')
]
