from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model"""
    is_email_verified = models.BooleanField('Почта подтверждена', default=False)

