import pytz
from django.utils import timezone

CARDS_PER_PAGE = 40
OLD_DATE = timezone.datetime(1970, 1, 1, tzinfo=pytz.UTC)
MAIL_SERVICES_LINKS = {
    'ya': ('Яндекс.Почту', 'mail.yandex.ru'),
    'yandex': ('Яндекс.Почту', 'mail.yandex.ru'),
    'gmail': ('почту Gmail', 'mail.google.com'),
    'mail': ('почту Mail.Ru', 'e.mail.ru'),
    'inbox': ('почту Mail.Ru', 'e.mail.ru'),
    'rambler': ('почту Rambler', 'mail.rambler.ru'),
    'yahoo': ('почту Yahoo', 'mail.yahoo.com')
}
