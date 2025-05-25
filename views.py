# pylint: disable=line-too-long

import importlib

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseServerError

def import_objects(request): # pylint: disable=too-many-branches
    if request.method == 'POST': # pylint: disable=too-many-nested-blocks
        file = request.FILES.get('import_file', None)
        file_type = request.POST.get('import_file_type', None)
        redirect_to = request.POST.get('import_file_next', None)

        if None in (file, file_type):
            messages.add_message(request, messages.ERROR, 'Unable to import objects - malformed request.')
        else:
            messages_added = 0

            for app in settings.INSTALLED_APPS:
                try:
                    docker_module = importlib.import_module('.docker_api', package=app)

                    import_messages = docker_module.import_objects(file_type, file)

                    if import_messages is not None:
                        for message in import_messages:
                            if isinstance(message, str):
                                messages.add_message(request, messages.INFO, message)
                            elif isinstance(message, (list, tuple)):
                                to_send = message[0]
                                level = messages.INFO

                                if len(message) > 1:
                                    level = message[1]

                                messages.add_message(request, level, to_send)

                                messages_added += 1

                        break
                except ImportError:
                    pass
                except AttributeError:
                    pass

            if messages_added == 0:
                messages.add_message(request, messages.WARNING, 'Unable to import file. Check that importer exists (%s) and can parse the uploaded file.' % file_type)

        if redirect_to is not None:
            return HttpResponseRedirect(redirect_to)

    return HttpResponseServerError() # HttpResponseRedirect(reverse('admin:index'))
