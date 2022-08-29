from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django_hosts import reverse_lazy

from app.forms import NewProductForm
from app.models import Product
from core.decorators import pc_redirect
from core.middleware import get_token


class HomeView(View):
    """Mobile home page"""

    template = 'app_mobile/homepage.html'
    pc_reverse = reverse_lazy('home', host='app')

    @pc_redirect(pc_reverse)
    def get(self, request):
        return render(request, self.template)


class AppView(LoginRequiredMixin, View):
    """Mobile fridge page"""

    template = 'app_mobile/app.html'
    form = NewProductForm
    pc_reverse = reverse_lazy('app', host='app')

    @pc_redirect(pc_reverse)
    def get(self, request, saved=None):
        context = {
            'form': self.form() if saved is None else self.form(request.POST),
            'token': get_token(),
            'saved': saved
        }
        return render(request, self.template, context)

    @pc_redirect(pc_reverse)
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


class PrivacyPolicyView(View):
    """Mobile privacy policy page"""

    template = 'app_mobile/privacy-policy.html'
    pc_reverse = reverse_lazy('privacy-policy', host='app')

    @pc_redirect(pc_reverse)
    def get(self, request):
        return render(request, self.template)
