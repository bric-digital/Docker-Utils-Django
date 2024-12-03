# pylint: disable=line-too-long

# Source: https://stackoverflow.com/a/72405135

import json
import os

from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('New secret key: %s' % get_random_secret_key())
