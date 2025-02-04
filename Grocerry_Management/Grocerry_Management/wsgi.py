import os
from django.core.wsgi import get_wsgi_application

# Ensure this points to the correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Grocerry_Management.settings')

application = get_wsgi_application()
