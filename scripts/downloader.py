#!/usr/bin/python

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statcast.settings")
from django.conf import settings


from statcast.monitor.models import *