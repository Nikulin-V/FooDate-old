from django.urls import path

from book.views import HomeView, ProductsView, RecipesView, ProductView, RecipeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<str:product_slug>', ProductView.as_view(), name='product'),
    path('recipes/', RecipesView.as_view(), name='recipes'),
    path('recipes/<str:recipe_slug>', RecipeView.as_view(), name='recipe'),
]
