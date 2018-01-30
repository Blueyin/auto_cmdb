#!/usr/bin/env python
import os
import sys
from celery import Celery, platforms
platforms.C_FORCE_ROOT = True

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CMDB.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
