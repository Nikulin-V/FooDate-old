from django.shortcuts import render
from django.views import View
from django_hosts import reverse_lazy

from app.forms import NewProductForm
from app.models import Product
from core.decorators import mobile_redirect
from core.middleware import get_token, user_exists_check


class HomeView(View):
    """Home page"""

    template = 'app/homepage.html'
    mobile_reverse = reverse_lazy('home', host='app_mobile')

    @mobile_redirect(mobile_reverse)
    def get(self, request):
        return render(request, self.template)


class AppView(View):
    """Fridge page"""

    template = 'app/app.html'
    form = NewProductForm
    mobile_reverse = reverse_lazy('app', host='app_mobile')

    @mobile_redirect(mobile_reverse)
    def get(self, request, saved=None):
        user_exists_check(request)
        context = {
            'form': self.form() if saved is None else self.form(request.POST),
            'token': get_token(),
            'saved': saved
        }
        return render(request, self.template, context)

    @mobile_redirect(mobile_reverse)
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
    """Privacy policy page"""

    template = 'app/privacy-policy.html'
    mobile_reverse = reverse_lazy('privacy-policy', host='app_mobile')

    @mobile_redirect(mobile_reverse)
    def get(self, request):
        return render(request, self.template)
