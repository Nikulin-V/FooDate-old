from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

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
            user.first_name = (
                form.cleaned_data['first_name']
                if form.cleaned_data['first_name']
                else user.first_name
            )
            user.last_name = (
                form.cleaned_data['last_name'] if form.cleaned_data['last_name'] else user.last_name
            )
            user.email = form.cleaned_data['email'] if form.cleaned_data['email'] else user.email
            user.save()
            return HttpResponseRedirect(reverse('profile'))

        context = {'form': form}
        return render(request, self.template, context)


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
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        context = {'form': form}
        return render(request, self.template, context)
