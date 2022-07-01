from django.shortcuts import render
from django.views import View

from app.models import ProductCard
from book.models import ProductCategory


class HomeView(View):
    template = 'book/homepage.html'

    def get(self, request):
        return render(request, self.template)


class ProductsView(View):
    template = 'book/products.html'

    def get(self, request):
        args = request.GET
        category_slug = args.get('category')
        subcategory_slug = args.get('subcategory')

        categories = ProductCategory.categories.get_active()

        if category_slug:
            product_cards = ProductCard.cards.only('name', 'image').filter(
                subcategory__category__slug=category_slug
            ).all()
        elif subcategory_slug:
            product_cards = ProductCard.cards.only('name', 'image').filter(
                subcategory__slug=subcategory_slug
            ).all()
        else:
            product_cards = ProductCard.cards.only('name', 'image').all()

        context = {
            'categories': categories,
            'products': product_cards.values('name', 'image')
        }

        return render(request, self.template, context)


class RecipesView(View):
    template = 'book/recipes.html'

    def get(self, request):
        return render(request, self.template)
