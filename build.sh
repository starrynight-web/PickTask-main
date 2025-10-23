#!/usr/bin/env bash
# build.sh

# Exit on error
set -e

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (safe: won't fail if already applied)
python manage.py migrate