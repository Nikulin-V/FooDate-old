from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import render
from django.views import View
# noinspection PyPackageRequirements
from slugify import slugify

from app.models import ProductCard
from book.forms import NewProductCardForm, NewRecipeForm
from book.models import ProductCategory, ProductPhoto, RecipeCategory, Recipe, RecipePhoto
from core.constants import CARDS_PER_PAGE
from foodate.settings import MEDIA_ROOT


class HomeView(View):
    """Book home page"""

    template = 'error_pages/development.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile
        )


class ProductsView(View):
    """Product cards catalog page"""

    template = 'book/products.html'
    template_mobile = 'book/mobile/products.html'
    form = NewProductCardForm

    def get(self, request, saved=None):
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
            'pages': max_page_number,
            'form': self.form() if saved is None else self.form(request.POST),
            'saved': saved
        }

        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile,
            context
        )

    def post(self, request):
        form = self.form(request.POST)
        saved = False
        if form.is_valid():
            subcategory = form.cleaned_data['subcategory']
            name = form.cleaned_data['name']
            designation = form.cleaned_data['designation']
            shelf_life = form.cleaned_data['shelf_life']
            shelf_life_after_opening = form.cleaned_data['shelf_life_after_opening']
            min_storage_temperature, max_storage_temperature = None, None
            if (form.cleaned_data['min_storage_temperature'] and
                    form.cleaned_data['max_storage_temperature']):
                min_storage_temperature, max_storage_temperature = sorted((
                    form.cleaned_data['min_storage_temperature'] or '',
                    form.cleaned_data['max_storage_temperature'] or ''
                ))
            elif (form.cleaned_data['min_storage_temperature'] or
                  form.cleaned_data['max_storage_temperature']):
                min_storage_temperature = (form.cleaned_data['min_storage_temperature'] or
                                           form.cleaned_data['max_storage_temperature'])
            storage_temperature_unit = form.cleaned_data['storage_temperature_unit']
            composition = form.cleaned_data['composition']
            energy_value = form.cleaned_data['energy_value']
            energy_value_unit = form.cleaned_data['energy_value_unit']
            proteins = form.cleaned_data['proteins']
            fats = form.cleaned_data['fats']
            carbohydrates = form.cleaned_data['carbohydrates']
            filepath = ''
            if request.FILES:
                file = request.FILES['image']
                fs = FileSystemStorage()
                extension = file.name.split('.')[-1]
                filepath = f'products/images/{slugify(name)}.{extension}'
                fs.save(f'{MEDIA_ROOT}/{filepath}', file)

            new_product_card = ProductCard.cards.create(
                name=name,
                designation=designation,
                subcategory=subcategory,
                shelf_life=shelf_life,
                shelf_life_after_opening=shelf_life_after_opening,
                min_storage_temperature=min_storage_temperature,
                max_storage_temperature=max_storage_temperature,
                storage_temperature_unit=storage_temperature_unit,
                composition=composition,
                energy_value=energy_value,
                energy_value_unit=energy_value_unit,
                proteins=proteins,
                fats=fats,
                carbohydrates=carbohydrates,
                image=filepath
            )
            new_product_card.save()
            saved = True

        return self.get(request, saved)


class ProductView(View):
    """Specified product card page"""

    template = 'book/product.html'
    template_mobile = 'book/mobile/product.html'

    def get(self, request, product_slug):
        product: ProductCard = ProductCard.cards.filter(slug=product_slug).first()
        if not product:
            raise Http404()
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
    """Recipes catalog page"""

    template = 'book/recipes.html'
    template_mobile = 'book/mobile/recipes.html'
    form = NewRecipeForm

    def get(self, request, saved=None):
        args = request.GET
        category_slug = args.get('category') or ''
        search = args.get('search') or ''
        cards_per_page = args.get('cardsPerPage')
        page = args.get('page')

        recipes = Recipe.recipes.get_recipes(search).only('name', 'slug', 'image')
        if category_slug:
            recipes = recipes.filter(category__slug__regex=category_slug)

        try:
            cards_per_page = int(cards_per_page)
        except TypeError:
            cards_per_page = CARDS_PER_PAGE
        except ValueError:
            cards_per_page = CARDS_PER_PAGE

        recipes_count = len(recipes)
        max_page_number = recipes_count // cards_per_page
        max_page_number += 1 if recipes_count % cards_per_page != 0 else 0

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

        recipes = recipes.values(
            'name', 'slug', 'image'
        )[cards_per_page * page:cards_per_page * (page + 1)]

        context = {
            'categories': RecipeCategory.categories.all(),
            'recipes': recipes,
            'cards_per_page': cards_per_page,
            'current_page': page + 1,
            'pages': max_page_number,
            'saved': saved,
            'form': self.form() if saved is None else self.form(request.POST),
        }

        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile,
            context
        )

    def post(self, request):
        form = self.form(request.POST)
        saved = False
        if form.is_valid():
            category = form.cleaned_data['category']
            name = form.cleaned_data['name']
            recipe = form.cleaned_data['recipe']
            energy_value = form.cleaned_data['energy_value']
            energy_value_unit = form.cleaned_data['energy_value_unit']
            people_count = form.cleaned_data['people_count']
            filepath = ''
            if request.FILES:
                file = request.FILES['image']
                fs = FileSystemStorage()
                extension = file.name.split('.')[-1]
                filepath = f'products/images/{slugify(name)}.{extension}'
                fs.save(f'{MEDIA_ROOT}/{filepath}', file)

            new_recipe = Recipe.recipes.create(
                category=category,
                name=name,
                recipe=recipe,
                energy_value=energy_value,
                energy_value_unit=energy_value_unit,
                people_count=people_count,
                image=filepath
            )
            new_recipe.save()
            saved = True

        return self.get(request, saved)


class RecipeView(View):
    template = 'book/recipe.html'
    template_mobile = 'book/mobile/recipe.html'

    def get(self, request, recipe_slug):
        recipe: Recipe = Recipe.recipes.filter(slug=recipe_slug).first()
        if not recipe:
            raise Http404()
        photos = RecipePhoto.objects.filter(recipe=recipe, is_published=True).all()
        context = {
            'recipe': recipe,
            'photos': photos
        }
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile,
            context
        )
