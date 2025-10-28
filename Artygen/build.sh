#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Test that Django can start (will show error if any)
echo "Testing Django configuration..."
python manage.py check --deploy
