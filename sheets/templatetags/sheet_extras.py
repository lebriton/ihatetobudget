import datetime

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def order_queryset_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def attrsum(container, attr_name):
    return sum(getattr(e, attr_name) for e in container)


@register.filter
@stringfilter
def currency(string):
    return f"{string.replace('.', ',')}€"  # TEMP:


@register.simple_tag
def setvar(val=None):
    return val


@register.filter
def is_future_date(date):
    return date > datetime.datetime.now().date()
