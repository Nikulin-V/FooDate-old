from django.shortcuts import render
from django.views import View


class HomeView(View):
    template = 'app_mobile/homepage.html'

    def get(self, request):
        return render(request, self.template)


class AppView(View):
    template = 'app_mobile/app.html'

    def get(self, request):
        return render(request, self.template)
