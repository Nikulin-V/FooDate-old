from django.core.validators import BaseValidator


class BiggerThanValidator(BaseValidator):
    def __init__(self, limit_value):
        self.limit_value = limit_value
        self.message = f'Убедитесь, что это значение больше {self.limit_value}'
        super().__init__(limit_value)

    def compare(self, a, b):
        return a <= b
