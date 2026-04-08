"""
ASGI config for vulnbank project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnbank.settings')
application = get_asgi_application()
