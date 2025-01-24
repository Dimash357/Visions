"""
WSGI config for django_settings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if 'admin' in os.getenv('DJANGO_SETTINGS_MODULE', ''):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../django_settings.admin_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../django_settings.settings')

application = get_wsgi_application()
