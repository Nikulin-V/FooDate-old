from django.contrib.auth import logout
from social_core.exceptions import AuthException


def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
        elif not user:
            user = social.user
    return {
        'social': social,
        'user': user,
        'is_new': user is None,
        'new_association': False
    }


def associate_by_email(backend, details, user=None, *args, **kwargs):
    if user:
        return None

    email = details.get('email')
    if email:
        if 'ya' not in email.split('@')[1]:
            users = list(backend.strategy.storage.user.get_users_by_email(email))
        else:
            new_email_login = email.split('@')[0]
            for domain in ['ya.ru', 'yandex.ru', 'yandex.by', 'yandex.com', 'yandex.kz']:
                new_email = '@'.join((new_email_login, domain))
                users = list(backend.strategy.storage.user.get_users_by_email(new_email))
                if users:
                    break
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given email address is associated with another account'
            )
        else:
            return {
                'user': users[0],
                'is_new': False
            }
