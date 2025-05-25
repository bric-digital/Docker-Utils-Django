# pylint: disable=line-too-long

from django import template
from django.template.loader import render_to_string
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def docker_utils_add_import_button(context):
    if hasattr(context['cl'].model_admin, 'portable_model_export_items'):
        template_dict = {}

        for context_dict in context.dicts:
            try:
                template_dict.update(context_dict)
            except ValueError:
                pass

        add_url = template_dict.get('add_url', None)

        if add_url is not None:
            item_type = add_url[7:-5].replace('/', '.')

            template_dict['docker_utils_item_type'] = item_type

            template_dict['docker_utils_import_file_next'] = context.request.META.get('HTTP_REFERER', reverse('admin:index'))

            return render_to_string('docker_utils/admin_import_button.html', context=template_dict, request=context.request)

    return ''
