from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
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
            user = get_user_model().objects.filter(
                **kwargs,
                is_email_verified=True
            ).first()
            if user is None:
                users = get_user_model().objects.filter(**kwargs)
                if len(users) == 1:
                    user = users[0]
                else:
                    raise get_user_model().DoesNotExist
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
