#!/bin/bash
# Production Deployment Script for Pen and I Publishing
LOG_FILE="/var/log/pen-deploy.log"
REPO_DIR="/home/pen"
PROJECT_NAME="pen"

echo "$(date): Starting production deployment..." >> $LOG_FILE

# Navigate to repository
cd $REPO_DIR

# Pull latest changes
git fetch origin
git reset --hard origin/main
echo "$(date): Git pull completed" >> $LOG_FILE

# Activate virtual environment
source venv/bin/activate
echo "$(date): Virtual environment activated" >> $LOG_FILE

# Install/update dependencies
pip install -r requirements.txt
echo "$(date): Dependencies updated" >> $LOG_FILE

# Collect static files
python manage.py collectstatic --noinput
echo "$(date): Static files collected" >> $LOG_FILE

# Run database migrations
python manage.py migrate
echo "$(date): Database migrations completed" >> $LOG_FILE

# Restart Gunicorn service
sudo systemctl restart ${PROJECT_NAME}.service
echo "$(date): Service restarted" >> $LOG_FILE

# Verify socket permissions
sudo chmod 666 ${REPO_DIR}/${PROJECT_NAME}.sock
sudo chgrp www-data ${REPO_DIR}/${PROJECT_NAME}.sock
echo "$(date): Socket permissions fixed" >> $LOG_FILE

echo "$(date): Production deployment completed successfully!"
