#!/bin/bash
# Quick setup script for Weather Comparison Bot

echo "🚀 Weather Comparison Bot - Quick Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo ""

# Prompt for Twilio credentials
echo "📱 Twilio Setup"
echo "==============="
echo "You'll need a Twilio account. Get one free at: https://www.twilio.com/try-twilio"
echo ""

read -p "Enter your Twilio Account SID: " ACCOUNT_SID
read -p "Enter your Twilio Auth Token: " AUTH_TOKEN
read -p "Enter your Twilio Phone Number (e.g., +15551234567): " TWILIO_PHONE
read -p "Enter your friend's phone number (e.g., +16171234567): " FRIEND_PHONE

echo ""
echo "Creating .env file..."

cat > .env << EOF
export TWILIO_ACCOUNT_SID="$ACCOUNT_SID"
export TWILIO_AUTH_TOKEN="$AUTH_TOKEN"
export TWILIO_PHONE_NUMBER="$TWILIO_PHONE"
export FRIEND_PHONE_NUMBER="$FRIEND_PHONE"
EOF

echo "✅ Environment file created!"
echo ""

# Make scripts executable
chmod +x weather_texter.py
chmod +x weather_texter_enhanced.py

echo "🧪 Running test (dry-run mode)..."
echo ""
source .env
python3 weather_texter_enhanced.py --dry-run

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "To send a test message:"
echo "  source .env && python3 weather_texter_enhanced.py"
echo ""
echo "To set up daily automation:"
echo "  See SETUP_GUIDE.md for scheduling instructions"
echo ""
echo "Your credentials are saved in .env"
echo "Run 'source .env' before running the script manually"
