#!/bin/bash

# Crypto X Analyzer Startup Script

echo "🚀 Starting Crypto X Analyzer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API credentials before running the app."
    echo "🔗 Get Twitter API access at: https://developer.twitter.com"
fi

# Run the application
echo "🌐 Starting Streamlit app..."
echo "📱 The app will open in your browser at http://localhost:8501"
streamlit run app.py