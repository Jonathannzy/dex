#!/bin/bash

# Hyperliquid PUMP Token Monitor Startup Script
# This script starts monitoring the PUMP token on Hyperliquid

echo "🚀 Hyperliquid PUMP Token Monitor"
echo "=================================="
echo ""
echo "Starting monitoring for PUMP token..."
echo "📊 Updates every 10 minutes with technical analysis"
echo "🛑 Press Ctrl+C to stop monitoring"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check if the monitor script exists
if [ ! -f "hyperliquid_simple_monitor.py" ]; then
    echo "❌ Error: hyperliquid_simple_monitor.py not found!"
    echo "Please make sure you're running this script from the correct directory."
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

echo "✅ Starting PUMP token monitor..."
echo ""

# Start the monitor
python3 hyperliquid_simple_monitor.py --token PUMP