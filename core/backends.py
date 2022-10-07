import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    This is a ModelBackend that allows authentication
    with either a username or an email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request: WSGIRequest
        :param username: str
        :param password: str
        :return: User or User.DoesNotExist
        """

        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(email_regex, username):
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.filter(
                **kwargs,
                is_email_verified=True
            ).first()
            if user is None:
                users = User.objects.filter(**kwargs)
                if len(users) == 1:
                    user = users[0]
                else:
                    raise User.DoesNotExist
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
