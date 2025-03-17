from django import template

register = template.Library()

@register.filter(name='review_nominative')
def review_nominative(value):
    value = int(value)
    if value == 0:
        return "отзывов"

    last_two = value % 100
    if 11 <= last_two <= 19:
        return "отзывов"

    last_digit = value % 10
    if last_digit == 1:
        return "отзыв"
    elif 2 <= last_digit <= 4:
        return "отзыва"
    else:
        return "отзывов"


@register.filter(name='review_prepositional')
def review_prepositional(value):
    try:
        num = int(value)
    except (TypeError, ValueError):
        return "отзывах"

    last_two = num % 100
    if 11 <= last_two <= 19:
        return "отзывах"

    last_digit = num % 10
    if last_digit == 1:
        return "отзыве"
    else:
        return "отзывах"


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg