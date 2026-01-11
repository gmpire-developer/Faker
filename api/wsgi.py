"""
WSGI config for Vercel deployment.
Configured to work with serverless environment.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django_app = get_wsgi_application()

# Wrap for Vercel serverless
def app(environ, start_response):
    """WSGI application for Vercel."""
    return django_app(environ, start_response)
