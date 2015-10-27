# -*- coding: utf-8 -*-
from decimal import Decimal


def round(value, prec=9, rounding='ROUND_HALF_EVEN'):
    return Decimal(value).quantize(Decimal('1e{0}'.format(-prec)), rounding)


def format_money(money_value, precision=2, thousands_separator=True):
    """Format money with comma instead of point
       Ex: 1234.56 -> 1.234,56
       :param money_value: Decimal or float
       :return: str
    """
    if isinstance(money_value, int):
        money_value = float(money_value)

    if not isinstance(money_value, (float, Decimal)):
        raise ValueError('Must be float or Decimal')

    mask = '{0:.%sf}' % str(precision)
    value = mask.format(money_value)
    integer_part, fractional_part = value.split('.')

    if thousands_separator:
        integer_part = '{0:,}'.format(int(integer_part)).replace(',', '.')

    return '{0},{1}'.format(integer_part, fractional_part)
