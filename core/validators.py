import datetime

import pytz
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from foodate.settings import TIME_ZONE


class BiggerThanValidator(BaseValidator):
    """Validates that field value is bigger than limit_value"""

    def __init__(self, limit_value):
        self.limit_value = limit_value
        self.message = f'Убедитесь, что это значение больше {self.limit_value}'
        super().__init__(limit_value)

    def compare(self, value, limit):
        return value <= limit


def date_in_past(value: datetime.datetime):
    """Validates that field date value is in past"""
    time_zone = pytz.timezone(TIME_ZONE)
    message = 'Убедитесь, что эти дата и время раньше или равны текущим'
    if value.astimezone(time_zone) > datetime.datetime.now().astimezone(time_zone):
        raise ValidationError(message)
