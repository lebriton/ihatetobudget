import datetime
import re

from django import template
from django.conf import settings
from django.http import QueryDict
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def order_queryset_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def attrsum(container, attr_name):
    return sum(getattr(e, attr_name) for e in container)


@register.filter
def currency(amount):
    return (
        settings.CURRENCY_PREFIX
        + f"{amount:,.2f}".translate(
            str.maketrans(
                ",.",
                settings.CURRENCY_GROUP_SEPARATOR
                + settings.CURRENCY_DECIMAL_SEPARATOR,
            )
        )
        + settings.CURRENCY_SUFFIX
    )


@register.simple_tag
def setvar(val=None):
    return val


@register.filter
def is_future_date(date):
    return date > datetime.datetime.now().date()


@register.filter
def is_current_month(date):
    today = datetime.datetime.today()
    return date.month == today.month and date.year == today.year


@register.filter
def override_query_dict(query_dict, parameters):
    query_dict = query_dict.copy()
    query_dict.update(QueryDict(parameters))
    return "&".join(f"{k}={v}" for k, v in query_dict.items())


@register.filter
@stringfilter
def highlight_text(text, term):
    return (
        mark_safe(
            re.sub(
                term,
                lambda matchobj: f'<span class="text-highlight">{matchobj.group(0)}</span>',  # noqa: E501
                text,
                flags=re.I,
            )
        )
        if term
        else text
    )
