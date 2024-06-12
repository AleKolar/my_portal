from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    banned_words = ['badword1', 'badword2']
    for word in banned_words:
        if isinstance(word, str):
            value = value.replace(word[1:], '*' * len(word[1:]))
    return value