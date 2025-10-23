#!/usr/bin/env bash
# build.sh - Simplified build script

set -o errexit

echo "🚀 Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Build completed!"