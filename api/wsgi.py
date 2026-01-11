"""
WSGI config for Vercel deployment.
Configured to work with serverless environment.
"""

import os
import sys
from pathlib import Path

# Add the project root to sys.path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI application after path is set
from django.core.wsgi import get_wsgi_application

# Initialize Django application
application = get_wsgi_application()

# Alias for Vercel
app = application
