from django.shortcuts import render
from django.views import View


class HomeView(View):
    template = 'book/homepage.html'

    def get(self, request):
        return render(request, self.template)


class ProductsView(View):
    template = 'book/products.html'

    def get(self, request):
        return render(request, self.template)


class RecipesView(View):
    template = 'book/recipes.html'

    def get(self, request):
        return render(request, self.template)
