#!/bin/bash
set -e

echo "=========================================="
echo "eBuilder Docker Entrypoint"
echo "=========================================="

# Fix permissions on mounted volumes (running as root initially)
chown -R appuser:appuser /app/staticfiles 2>/dev/null || true
chown -R appuser:appuser /app/db 2>/dev/null || true
chown -R appuser:appuser /app/media 2>/dev/null || true
chown -R appuser:appuser /app/logs 2>/dev/null || true

# Switch to appuser for all Django commands
INIT_MARKER="/app/db/.initialized"

if [ ! -f "$INIT_MARKER" ]; then
    echo "First boot detected"

    gosu appuser python manage.py migrate --noinput
    
    # Configure Django Sites framework with customer domain
    gosu appuser python -c "
import django; django.setup()
from django.contrib.sites.models import Site
import os
Site.objects.update_or_create(
    id=1,
    defaults={
        'domain': os.environ.get('SHOP_DOMAIN', 'localhost'),
        'name': os.environ.get('SITE_NAME', 'My Shop')
    }
)
print(f\"Site configured: {os.environ.get('SHOP_DOMAIN', 'localhost')}\")"

    if [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
        gosu appuser python manage.py create_admin_from_env
    fi

    gosu appuser python manage.py collectstatic --noinput

    echo "$(date -Iseconds)" > "$INIT_MARKER"
    chown appuser:appuser "$INIT_MARKER"
else
    gosu appuser python manage.py migrate --noinput
fi

# ALWAYS ensure static files are present
gosu appuser python manage.py collectstatic --noinput

# Run gunicorn as appuser
exec gosu appuser gunicorn ebuilder.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3