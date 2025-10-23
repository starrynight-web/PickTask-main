set -o errexit

echo "==========================================="
echo "🚀 Starting PickTask Build Process"
echo "==========================================="

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗃️ Creating database migrations..."
python manage.py makemigrations home authentication workspace --noinput

echo "🔄 Applying migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "==========================================="
echo "✅ Build completed successfully!"
echo "==========================================="