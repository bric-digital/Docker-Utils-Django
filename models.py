from django.conf import settings
from django.core.checks import Warning, register # pylint: disable=redefined-builtin
from django.urls import reverse, NoReverseMatch

@register()
def check_settings_order(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    try:
        docker_index = settings.INSTALLED_APPS.index('docker_utils')
        admin_index = settings.INSTALLED_APPS.index('django.contrib.admin')

        if admin_index < docker_index:
            error = Warning('Incorrect INSTALLED_APPS order.', hint='Verify that docker_utils is before django.contrib.admin in INSTALLED_APPS.', obj=None, id='docker_utils.W001')
            errors.append(error)
    except ValueError:
        error = Warning('Missing docker_utils in INSTALLED_APPS.', hint='Verify that docker_utils is included in INSTALLED_APPS.', obj=None, id='docker_utils.W002')
        errors.append(error)

    return errors

@register()
def check_docker_utils_urls(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    try:
        reverse('docker_utils_import_objects')
    except NoReverseMatch:
        error = Warning('Missing docker_utils_import_objects path.', hint='Verify docker_utils is included in the site\'s urls.py.', obj=None, id='docker_utils.W003')
        errors.append(error)

    return errors
