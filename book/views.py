from django.db.models import Q
from django.shortcuts import render
from django.views import View

from app.models import ProductCard
from book.models import ProductCategory
from core.constants import CARDS_PER_PAGE


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
        cards_per_page = args.get('cardsPerPage')
        page = args.get('page')

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

        try:
            cards_per_page = int(cards_per_page)
        except TypeError:
            cards_per_page = CARDS_PER_PAGE
        except ValueError:
            cards_per_page = CARDS_PER_PAGE

        product_cards_count = len(product_cards)
        max_page_number = product_cards_count // cards_per_page
        max_page_number += 1 if product_cards_count % cards_per_page != 0 else 0

        try:
            page = int(page)
            if 1 <= int(page) <= max_page_number:
                page = int(page) - 1
            else:
                page = 0
        except TypeError:
            page = 0
        except ValueError:
            page = 0

        product_cards = (
            product_cards.values('name', 'image')[cards_per_page * page:cards_per_page * (page + 1)]
        )

        context = {
            'categories': categories,
            'products': product_cards,
            'cards_per_page': cards_per_page,
            'current_page': page + 1,
            'pages': max_page_number
        }

        template = self.template if request.user_agent.is_pc else self.template_mobile

        return render(request, template, context)


class RecipesView(View):
    template = 'book/recipes.html'

    def get(self, request):
        return render(request, self.template)
