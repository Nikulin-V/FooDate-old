from threading import current_thread
from uuid import uuid4

from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token

import users.models

User = get_user_model()
_requests = {}


def user_exists_check(request):
    if request.user == AnonymousUser():
        if 'username' not in request.session:
            request.session['username'] = f'Гость_{uuid4()}'
            guest_user = create_account_by_session(request)
        else:
            try:
                guest_user = User.objects.get(username=request.session['username'])
            except users.models.User.DoesNotExist:
                guest_user = create_account_by_session(request)
        login(request, guest_user, 'core.backends.EmailAuthBackend')
    elif 'username' not in request.session:
        request.session['username'] = request.user.username


def create_account_by_session(request):
    return User.objects.create(username=request.session['username'])


def get_token():
    """Returns user's api token"""
    return Token.objects.get_or_create(user=get_user())[0]


def get_user():
    """Returns current user model"""
    thread = current_thread()
    if thread not in _requests:
        return None
    return _requests[thread].user


class RequestMiddleware(MiddlewareMixin):
    """Middleware that helps to define current user"""
    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        _requests[current_thread()] = request
