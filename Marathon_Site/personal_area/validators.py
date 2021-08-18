import datetime

from django.core.exceptions import ValidationError


def validate_date(value):
    today = datetime.date.today()
    if value < today:
        raise ValidationError(u'\"%s\" нельзя выбрать число, которое уже прошло!' % value)


def validate_price(value):
    if value == 0:
        return
    if value < 100:
        raise ValidationError(u'\"%s\" нельзя выбрать цену, меньше 100!' % value)
