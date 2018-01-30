#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from app.backend.tasks import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMDB.settings')

app = Celery('CMDB')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#@app.task(bind=True)
#def debug_task(self):
#    print('Request: {0!r}'.format(self.request))
