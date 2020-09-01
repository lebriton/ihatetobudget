from django import template

register = template.Library()


@register.filter
def order_queryset_by(queryset, order):
    return queryset.order_by(order)
