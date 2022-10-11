from django.contrib.auth import get_user_model


def is_email_used(email):
    return len(get_user_model().objects.filter(email=email, is_email_verified=True)) != 0
