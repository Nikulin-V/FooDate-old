from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    This is a ModelBackend that allows authentication
    with either a username or an email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
