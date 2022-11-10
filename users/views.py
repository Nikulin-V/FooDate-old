from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django_email_verification import send_email, verify_view
from django_hosts import reverse
from social_django.models import UserSocialAuth

from core.constants import MAIL_SERVICES_LINKS
from users.forms import UserRegistrationForm, UserChangeForm
from users.utils import is_email_used, is_guest_username

User = get_user_model()


class ProfileView(LoginRequiredMixin, View):
    """User profile page"""

    template = 'users/profile.html'
    form = UserChangeForm

    def get(self, request):
        user = request.user
        connected_social_auths = UserSocialAuth.objects.filter(user=user).values_list('provider', flat=True)
        form = ProfileView.form(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        )
        context = {'form': form, 'social': connected_social_auths}
        return render(request, self.template, context)

    def post(self, request):
        user = request.user
        form = ProfileView.form(request.POST)
        context = {'form': form, 'errors': []}
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name'] or user.first_name
            user.last_name = form.cleaned_data['last_name'] or user.last_name
            new_email = form.cleaned_data['email']
            if user.email != new_email:
                if not is_email_used(new_email):
                    user.email = new_email
                    user.is_email_verified = False
                else:
                    context['errors'].append('Пользователь с таким email уже существует.')
            user.save()
            return HttpResponseRedirect(reverse('profile'))
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
        context = {'form': form, 'errors': []}
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            if not is_guest_username(username):
                if not is_email_used(email):
                    user = User.objects.create(
                        username=form.cleaned_data['username'],
                        email=email,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                    )
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    if request.user and not request.user.is_anonymous and request.user.is_guest:
                        request.user.delete()
                    send_email(user)
                    login(request, user, backend='core.backends.EmailAuthBackend')
                    return HttpResponseRedirect(reverse('profile'))
                else:
                    context['errors'].append('Пользователь с таким email уже существует.')
            else:
                context['errors'].append(
                    'Имена пользователей с префиксом "Гость" используются только гостевыми аккаунтами'
                )
        return render(request, self.template, context)


class EmailVerifyView(View):
    template = 'users/email_verify.html'

    def get(self, request):
        user = request.user
        context = {
            'email_verified': user.is_email_verified,
            'errors': []
        }
        if not is_email_used(user.email):
            if not user.is_email_verified:
                send_email(user)
                email_domain = user.email.split('@')[1].split('.')[0]
                email_service, email_link = MAIL_SERVICES_LINKS.get(email_domain)
                context['email_link'] = f'https://{email_link}'
                context['email_service'] = email_service
        else:
            context['errors'].append(
                'Пользователь с таким подтверждённым email уже существует.\n'
                'Если это ваш email, напишите на support@foodate.ru'
            )
        return render(request, self.template, context)


class TokenVerifyView(LoginRequiredMixin, View):
    """Page of verifying email confirmation token"""

    @verify_view
    def get(self, request, token):
        verify_view(token)
        return HttpResponseRedirect(reverse('email_verify'))


class CustomLoginView(LoginView):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user_ = request.user
        if not user_.is_anonymous:
            user_.save()
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        temp = super().dispatch(request, *args, **kwargs)
        if isinstance(temp, HttpResponseRedirect):
            if user_ and not user_.is_anonymous and user_.is_guest:
                user_.delete()
        return temp
