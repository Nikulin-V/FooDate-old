from django.shortcuts import render
from django.views import View


class HomeView(View):
    template = 'error_pages/development.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile
        )


class AppView(View):
    template = 'app/app.html'
    template_mobile = 'error_pages/development.html'

    def get(self, request):
        return render(
            request,
            self.template if request.user_agent.is_pc else self.template_mobile
        )
