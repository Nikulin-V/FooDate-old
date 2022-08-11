from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django_email_verification import send_email

from users.forms import UserRegistrationForm, UserChangeForm

User = get_user_model()


class ProfileView(LoginRequiredMixin, View):
    """User profile page"""

    template = 'users/profile.html'
    form = UserChangeForm

    def get(self, request):
        user = request.user

        form = ProfileView.form(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        )
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        user = request.user
        form = ProfileView.form(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name'] or user.first_name
            user.last_name = form.cleaned_data['last_name'] or user.last_name
            user.save()
            return HttpResponseRedirect(reverse('profile'))
        context = {'form': form}
        return render(request, self.template, context)


class SignupView(View):
    """Registration page"""

    template = 'users/signup.html'

    def get(self, request):
        form = UserRegistrationForm()
        context = {'form': form, 'registered': False}
        return render(request, self.template, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            send_email(user)
            context = {'registered': True}
            return render(request, self.template, context)
        context = {'form': form, 'registered': False}
        return render(request, self.template, context)
