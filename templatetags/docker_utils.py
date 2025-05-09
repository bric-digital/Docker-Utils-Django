import importlib
import json
import logging

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def docker_util_admin_list_tools(context):
    logging.warning('docker_util_admin_list_tools: %s', context)

    return ''
