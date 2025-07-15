# pylint: disable=line-too-long

import importlib
import json

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.exceptions import NotRegistered
from django.contrib.admin.sites import site as default_site
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.text import slugify

class PortableModelAdmin(admin.ModelAdmin):
    def portable_model_export_items(self, request, queryset): # pylint: disable=unused-argument, no-self-use
        all_exported_items = []

        filename = None

        for app in settings.INSTALLED_APPS:
            try:
                docker_module = importlib.import_module('.docker_api', package=app)

                if filename is None:
                    filename = '%s_%s.json' % (app, slugify(queryset.model.__name__))

                exported_objects = docker_module.export_objects(queryset, queryset.model.__name__)

                all_exported_items.extend(exported_objects)
            except ImportError:
                pass
            except AttributeError:
                pass

        if filename is None:
            filename = 'exported-items.json'

        response = HttpResponse(json.dumps(all_exported_items, indent=2), content_type='application/json', status=200)
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

def get_model_admin(admin_site, model): # pylint: disable=protected-access
    try:
        return admin_site._registry[model]
    except KeyError as exc:
        raise NotRegistered(f"The model {model.__name__} is not registered.") from exc

def reset_and_send_password(modeladmin, request, queryset): # pylint: disable=unused-argument
    for user in queryset:
        if user.email in (None, ''):
            messages.add_message(request, messages.ERROR, 'Unable to send password to "%s". No e-mail address set.' % user)
        else:
            password = get_random_string(16)

            context = {
                'user': user,
                'hostname': settings.ALLOWED_HOSTS[0],
                'site_url': 'https://%s/' % settings.ALLOWED_HOSTS[0],
                'admin_name': settings.ADMINS[0][0],
                'password': password,
            }

            subject = render_to_string('docker_utils/new_password_subject.txt', context)
            body = render_to_string('docker_utils/new_password_body.txt', context)

            from_address = settings.ADMINS[0][1]

            send_mail(subject, body, from_address, [user.email])

            user.set_password(password)
            user.save()

            messages.add_message(request, messages.INFO, 'Sent new random password to "%s".' % user)

reset_and_send_password.short_description = 'Reset and send user password'

user_admin = get_model_admin(default_site, get_user_model())

user_admin.actions = list(user_admin.actions)
user_admin.actions.append(reset_and_send_password)
