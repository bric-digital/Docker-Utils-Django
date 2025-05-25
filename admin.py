# pylint: disable=line-too-long

import importlib
import json

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import slugify

class PortableModelAdmin(admin.ModelAdmin):
    def portable_model_export_items(self, request, queryset): # pylint: disable=unused-argument
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
