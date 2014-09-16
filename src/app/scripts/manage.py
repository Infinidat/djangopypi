#
# This replaces Django's default manage.py, and is called from bin/manage
#

import os
import sys

def execute():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
