from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model"""
    is_email_verified = models.BooleanField('Почта подтверждена', default=False)
    beta_testing = models.BooleanField('Хочу участвовать в бета-тестировании', default=False)
    customer_development_interview = models.BooleanField(
        'Готов поговорить об опыте использования похожих сервисов (доставка, кулинария, фудшеринг)',
        default=False
    )

    @property
    def is_guest(self):
        return self.username.startswith('Гость_')
