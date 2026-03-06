#!/bin/bash
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

echo "======================================"
echo "  AlfaXMusic - Telegram Music Bot"
echo "  Powered by Alfa Bots"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your credentials."
        exit 1
    else
        echo "❌ .env.example not found. Please create a .env file manually."
        exit 1
    fi
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p assets

echo ""
echo "======================================"
echo "  Starting AlfaXMusic Bot..."
echo "======================================"
echo ""

# Run the bot
python3 -m AlfaXmusic
