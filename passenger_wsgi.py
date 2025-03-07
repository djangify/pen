import os
import sys

# Use the correct Python interpreter path from your .htaccess
INTERP = "/home/penpub24/virtualenv/pen/3.10/bin/python"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set up paths and environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pen'))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'pen.settings'

# Import and create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
