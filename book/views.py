from django.db.models import Q
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
    template_mobile = 'book/mobile/products.html'

    def get(self, request):
        args = request.GET
        category_slug = args.get('category')
        subcategory_slug = args.get('subcategory')
        search = args.get('search')

        categories = ProductCategory.categories.get_active()
        product_cards = ProductCard.cards.only('name', 'image').all()

        if category_slug:
            product_cards = product_cards.only('name', 'image').filter(
                subcategory__category__slug=category_slug
            ).all()
        if subcategory_slug:
            product_cards = product_cards.only('name', 'image').filter(
                subcategory__slug=subcategory_slug
            ).all()
        if search:
            product_cards = product_cards.filter(
                Q(name__iregex=search) or Q(slug__iregex=search) or
                Q(designation__iregex=search) or Q(subcategory__category__name__iregex=search)
                or Q(subcategory__name__iregex=search)
            )

        context = {
            'categories': categories,
            'products': product_cards.values('name', 'image')
        }

        template = self.template if request.user_agent.is_pc else self.template_mobile

        return render(request, template, context)


class RecipesView(View):
    template = 'book/recipes.html'

    def get(self, request):
        return render(request, self.template)
