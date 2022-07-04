from django.shortcuts import render
from django.views import View

from app.models import ProductCard
from book.models import ProductCategory, ProductPhoto
from core.constants import CARDS_PER_PAGE


class HomeView(View):
    template = 'error_pages/development.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile
        )


class ProductsView(View):
    template = 'book/products.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        args = request.GET
        category_slug = args.get('category') or ''
        subcategory_slug = args.get('subcategory') or ''
        search = args.get('search') or ''
        cards_per_page = args.get('cardsPerPage')
        page = args.get('page')

        categories = ProductCategory.categories.get_active()

        product_cards = ProductCard.cards.search(search).only('name', 'slug', 'image').filter(
            subcategory__category__slug__regex=category_slug,
            subcategory__slug__regex=subcategory_slug
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

        product_cards = product_cards.values(
            'name', 'slug', 'image'
        )[cards_per_page * page:cards_per_page * (page + 1)]

        context = {
            'categories': categories,
            'products': product_cards,
            'cards_per_page': cards_per_page,
            'current_page': page + 1,
            'pages': max_page_number
        }

        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile,
            context
        )


class ProductView(View):
    template = 'book/product.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request, product_slug):
        product: ProductCard = ProductCard.cards.filter(slug=product_slug).first()
        photos = ProductPhoto.objects.filter(product=product, is_published=True).all()
        context = {
            'product': product,
            'photos': photos
        }
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile,
            context
        )


class RecipesView(View):
    template = 'error_pages/development.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile
        )
