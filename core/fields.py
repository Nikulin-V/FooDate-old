from django.utils.translation import gettext_lazy as _
from hcaptcha.fields import hCaptchaField


class CustomCaptchaField(hCaptchaField):
    default_error_messages = {
        'error_hcaptcha': _('Произошла ошибка. Попробуйте ещё раз'),
        'invalid_hcaptcha': _('Капча введена неверно. Попробуйте ещё раз'),
        'required': _('Докажите, что Вы человек'),
    }
