#!/usr/bin/env bash
# Lexsy Backend - Render Build Script
# This script runs on Render during the build phase

set -o errexit  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔨 Lexsy Backend Build Starting..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# 2. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# 3. Create necessary directories
echo "📁 Creating application directories..."
mkdir -p uploads
mkdir -p processed
mkdir -p logs

echo "✅ Uploads directory created"
echo "✅ Processed directory created"
echo "✅ Logs directory created"

# 4. Verify critical dependencies
echo "🔍 Verifying critical dependencies..."
python -c "import flask; print('✅ Flask:', flask.__version__)"
python -c "import groq; print('✅ Groq installed')"
python -c "import docx; print('✅ python-docx installed')"
python -c "import gunicorn; print('✅ Gunicorn installed')"

# 5. Display Python version
echo "🐍 Python version:"
python --version

# 6. Check if firebase-admin is available (optional)
if python -c "import firebase_admin" 2>/dev/null; then
    echo "✅ Firebase Admin SDK installed"
else
    echo "⚠️  Firebase Admin SDK not installed (optional)"
fi

# 7. Check if redis is available (optional)
if python -c "import redis" 2>/dev/null; then
    echo "✅ Redis client installed"
else
    echo "⚠️  Redis client not installed (optional)"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Build completed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

