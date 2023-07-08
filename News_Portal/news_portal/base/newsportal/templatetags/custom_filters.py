from django import template

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
