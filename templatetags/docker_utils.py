import importlib
import json
import logging

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def docker_utils_add_import_button(context):
    logging.warning('docker_utils_add_import_button: %s', context['cl'].model_admin)

    if hasattr(context['cl'].model_admin, 'portable_model_export_items'):
        return mark_safe('<a role="button" href="#" class="addlink">Import</a>')

    return ''
