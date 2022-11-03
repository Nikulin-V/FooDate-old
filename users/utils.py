from django.contrib.auth import get_user_model


def is_email_used(email: str):
    return len(get_user_model().objects.filter(email=email, is_email_verified=True)) != 0


def is_guest_username(username: str):
    return username.startswith('Гость_')
