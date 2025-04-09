# pylint: disable=line-too-long

# Source: https://stackoverflow.com/a/72405135

import json
import logging
import os

from django.core.management.commands import loaddata
from django.apps import apps

logger = logging.getLogger(__name__) # pylint: disable=invalid-name

def should_add_record(record):
    arr = record['model'].split('.')

    model_class = apps.get_model(app_label=arr[0], model_name=arr[1])

    return not model_class.objects.filter(id=record['pk'],).exists()

class Command(loaddata.Command):
    def handle(self, *args, **options):
        args = list(args)

        for file_name in args:
            # Read the original JSON file

            with open(file_name, encoding='utf-8') as json_file:
                json_list = json.load(json_file)

            # Filter out records that already exists
            json_list_filtered = list(filter(should_add_record, json_list))

            if not json_list_filtered:
                root_logger = logging.getLogger('')

                if options['verbosity'] > 0:
                    root_logger.setLevel(logging.INFO)

                logger.info('Skip %s...', file_name)

                continue

            # Write the updated JSON file
            file_dir_and_name, file_ext = os.path.splitext(file_name)

            file_name_temp = '%s_temp_%s' % (file_dir_and_name, file_ext,)

            with open(file_name_temp, 'w', encoding='utf-8') as json_file_temp:
                json.dump(json_list_filtered, json_file_temp)

            # Pass the request to the actual loaddata (parent functionality)
            # args[0] = file_name_temp
            super().handle(file_name_temp, **options) # pylint: disable=missing-super-argument

            # You can choose to not delete the file so that you can see what was added to your records
            os.remove(file_name_temp)
