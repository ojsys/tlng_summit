#!/bin/bash

# Nigeria Transport and Logistics Summit - Deployment Script
# This script helps automate the deployment process for cPanel hosting

echo "Nigeria Transport and Logistics Summit - Deployment Script"
echo "========================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Please copy .env.example to .env and configure your environment variables."
    echo "cp .env.example .env"
    exit 1
fi

# Set production settings
export DJANGO_SETTINGS_MODULE=tlng_summit_project.settings_production

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (if needed)
echo ""
echo "Would you like to create a superuser? (y/n)"
read -r create_superuser

if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Check if directories exist
echo "Checking directory structure..."
if [ ! -d "public_html" ]; then
    mkdir -p public_html/static
    mkdir -p public_html/media
    echo "Created public_html directories"
fi

if [ ! -d "logs" ]; then
    mkdir -p logs
    echo "Created logs directory"
fi

if [ ! -d "cache" ]; then
    mkdir -p cache
    echo "Created cache directory"
fi

# Set permissions
echo "Setting file permissions..."
chmod 755 passenger_wsgi.py
chmod -R 755 public_html/
chmod 600 .env 2>/dev/null || echo "Warning: Could not set .env permissions"

echo ""
echo "Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Upload all files to your cPanel hosting"
echo "2. Configure your domain to point to the project root"
echo "3. Set up your database credentials in .env"
echo "4. Test your deployment"
echo ""
echo "For detailed instructions, see DEPLOYMENT_GUIDE.md"