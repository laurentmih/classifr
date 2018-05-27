import django_heroku
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Activate Django-Heroku.
# Also initiates DB
django_heroku.settings(locals())