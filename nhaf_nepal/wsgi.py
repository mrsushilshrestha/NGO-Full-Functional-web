"""
WSGI config for NHAF Nepal project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nhaf_nepal.settings')
application = get_wsgi_application()
