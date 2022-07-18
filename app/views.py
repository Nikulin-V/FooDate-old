from django.shortcuts import render
from django.views import View

from app.forms import NewProductForm
from app.models import Product


class HomeView(View):
    template = 'app/homepage.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile
        )


class AppView(View):
    template = 'app/app.html'
    template_mobile = 'error_pages/development.html'
    form = NewProductForm

    def get(self, request, saved=None):
        context = {
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
            product_card = form.cleaned_data['product_card']
            amount = form.cleaned_data['amount']
            amount_unit = form.cleaned_data['amount_unit']
            production_date = form.cleaned_data['production_date']
            purchase_date = form.cleaned_data['purchase_date']

            new_product = Product.products.create(
                product_card=product_card,
                amount=amount,
                amount_unit=amount_unit,
                production_date=production_date,
                purchase_date=purchase_date
            )
            new_product.save()
            saved = True

        return self.get(request, saved)
