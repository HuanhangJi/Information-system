#coding:utf-8

from django import template

register = template.Library()

@register.filter
def test(value, args):
    return round(value * args,1)