from django.shortcuts import render
from django.views import View
from django_hosts import reverse_lazy

from core.decorators import pc_redirect


class HomeView(View):
    template = 'app_mobile/homepage.html'
    pc_reverse = reverse_lazy('home', host='app')

    @pc_redirect(pc_reverse)
    def get(self, request):
        return render(request, self.template)


class AppView(View):
    template = 'error_pages/development.html'
    pc_reverse = reverse_lazy('app', host='app')

    @pc_redirect(pc_reverse)
    def get(self, request):
        return render(request, self.template)
