#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
import traceback

# Add your site directory to the Python path
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, SITE_ROOT)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pen.settings')

# Create some test log files directly
with open(os.path.join(SITE_ROOT, 'django_debug.log'), 'a') as f:
    f.write("\n--- Starting debug run ---\n")
    try:
        # Try to initialize Django
        f.write("Initializing Django...\n")
        django.setup()
        f.write(f"Django version: {django.get_version()}\n")
        
        # Check if settings loaded
        f.write(f"DEBUG setting: {settings.DEBUG}\n")
        f.write(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}\n")
        
        # Check installed apps
        f.write("Installed apps:\n")
        for app in settings.INSTALLED_APPS:
            f.write(f"  - {app}\n")
        
        # Check database connection
        f.write("Testing database connection...\n")
        from django.db import connection
        connection.ensure_connection()
        f.write("Database connection successful!\n")
        
        # Check if models can be loaded
        f.write("Testing model imports...\n")
        from prompt.models import PromptCategory, WritingPrompt
        f.write(f"Prompt: {PromptCategory.objects.count()}\n")
        f.write(f"Writing: {WritingPrompt.objects.count()}\n")
        
        # Try to load WSGI application
        f.write("Testing WSGI application...\n")
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        f.write("WSGI application loaded successfully\n")
        
        # Try to render a simple template
        f.write("Testing template rendering...\n")
        from django.template import engines
        django_engine = engines['django']
        template = django_engine.from_string("Hello {{ name }}")
        rendered = template.render({"name": "World"})
        f.write(f"Template rendered: {rendered}\n")
        
        # Try URL resolution
        f.write("Testing URL resolution...\n")
        from django.urls import resolve, Resolver404
        try:
            match = resolve('/')
            f.write(f"Root URL resolves to: {match.func.__name__}\n")
        except Resolver404:
            f.write("Root URL does not resolve!\n")
        
        f.write("All tests completed successfully!\n")
        
    except Exception as e:
        f.write(f"ERROR: {str(e)}\n")
        f.write(traceback.format_exc())

print("Debug script completed. Check django_debug.log for results.")