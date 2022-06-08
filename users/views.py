from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from users.forms import UserRegistrationForm

User = get_user_model()


class SignupView(View):
    """Registration page"""
    template = 'users/signup.html'

    def get(self, request):
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
        context = {'form': form}
        return render(request, self.template, context)
