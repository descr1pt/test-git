from django import template
from datetime import datetime

register = template.Library()

ban_words = [
    'редиска',
    'картошка',
    'огурец',
]


@register.filter()
def censor(value: str):
    for a in ban_words:
        value = value.lower().replace(a.lower()[1:], '*'*len(a[1:]))
    return value


@register.filter()
def current_time(time, format_string='%d %b  %Y'):
    time = time.strftime(format_string)
    return time
