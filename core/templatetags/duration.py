import datetime

import pymorphy2 as pymorphy2
from django import template

register = template.Library()
morph = pymorphy2.MorphAnalyzer()


@register.filter
def duration(duration_date_time: datetime.timedelta):
    d = duration_date_time
    hours = d.seconds // 3600
    minutes = d.seconds // 60 % 60
    seconds = d.seconds % 3600 % 60
    days_word = morph.parse('день')[0].make_agree_with_number(d.days).word
    hours_word = morph.parse('час')[0].make_agree_with_number(hours).word
    minutes_word = morph.parse('минута')[0].make_agree_with_number(minutes).word
    seconds_word = morph.parse('секунда')[0].make_agree_with_number(seconds).word
    return f'{f"{d.days} {days_word} " if d.days else ""}' \
           f'{f"{hours} {hours_word} " if hours else ""}' \
           f'{f"{minutes} {minutes_word} " if minutes else ""}' \
           f'{f"{seconds} {seconds_word} " if seconds else ""}'
