import pytz
from django.utils import timezone

OLD_DATE = timezone.datetime(1970, 1, 1, tzinfo=pytz.UTC)
GUEST_LIFETIME_HOURS = 4
