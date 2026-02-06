# Weather Comparison Texting Bot - Setup Guide

## Overview
This bot automatically sends daily playful weather comparisons between Del Mar, CA and Boston, MA via SMS.

## Prerequisites

### 1. Python 3.7+
Check your version: `python3 --version`

### 2. Required Python Packages
```bash
pip install requests twilio
```

## Setup Instructions

### Step 1: Get Twilio Account (for SMS)

1. Sign up at https://www.twilio.com/try-twilio
2. Free trial includes $15 credit (enough for ~500 messages)
3. Get your credentials from the Twilio Console:
   - Account SID
   - Auth Token
   - Twilio Phone Number (provided during setup)

**Note:** With a trial account, you can only send to verified phone numbers. Verify your friend's number in the Twilio Console.

### Step 2: Configure the Script

Edit `weather_texter.py` and update these lines:

```python
TWILIO_ACCOUNT_SID = "your_account_sid_here"      # From Twilio Console
TWILIO_AUTH_TOKEN = "your_auth_token_here"        # From Twilio Console
TWILIO_PHONE_NUMBER = "+15551234567"              # Your Twilio number
FRIEND_PHONE_NUMBER = "+16171234567"              # Friend's number (include +1)
```

### Step 3: Test the Script

Run manually to test:
```bash
python3 weather_texter.py
```

You should see output like:
```
🤖 Weather Comparison Bot Starting - 2026-02-06 10:00:00
📡 Fetching Del Mar weather...
📡 Fetching Boston weather...
✍️  Generating playful message...

==================================================
MESSAGE PREVIEW:
==================================================
☀️ *California Weather Report* ☀️

It's a balmy 68°F here while you're freezing at 28°F...
==================================================

📱 Sending SMS...
✅ Message sent! SID: SM1234567890abcdef
✅ Done!
```

## Scheduling Options

### Option A: macOS/Linux - Using Cron

1. Make script executable:
```bash
chmod +x weather_texter.py
```

2. Open crontab:
```bash
crontab -e
```

3. Add this line to run daily at 9 AM:
```
0 9 * * * /usr/bin/python3 /path/to/weather_texter.py >> /path/to/weather_bot.log 2>&1
```

Replace `/path/to/` with your actual path.

**Cron Schedule Examples:**
- `0 9 * * *` - Every day at 9:00 AM
- `0 8 * * 1-5` - Weekdays at 8:00 AM
- `0 10 * * *` - Every day at 10:00 AM

### Option B: Windows - Using Task Scheduler

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name: "Weather Comparison Bot"
4. Trigger: Daily at desired time
5. Action: Start a Program
   - Program: `python`
   - Arguments: `C:\path\to\weather_texter.py`
6. Finish and test

### Option C: Cloud Hosting (Recommended for Reliability)

#### Using GitHub Actions (Free!)

1. Create a GitHub repository
2. Add your script to the repo
3. Add Twilio credentials as GitHub Secrets:
   - Settings → Secrets → Actions → New repository secret
   - Add: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE`, `FRIEND_PHONE`

4. Create `.github/workflows/daily-weather.yml`:

```yaml
name: Daily Weather Text

on:
  schedule:
    - cron: '0 17 * * *'  # 9 AM PST = 5 PM UTC
  workflow_dispatch:  # Allows manual trigger

jobs:
  send-weather:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install requests twilio
      - name: Send weather text
        env:
          TWILIO_ACCOUNT_SID: ${{ secrets.TWILIO_ACCOUNT_SID }}
          TWILIO_AUTH_TOKEN: ${{ secrets.TWILIO_AUTH_TOKEN }}
          TWILIO_PHONE_NUMBER: ${{ secrets.TWILIO_PHONE }}
          FRIEND_PHONE_NUMBER: ${{ secrets.FRIEND_PHONE }}
        run: |
          # Modify script to use environment variables
          python weather_texter.py
```

5. Modify the script to read from environment variables (see below)

## Using Environment Variables (More Secure)

Update the configuration section in `weather_texter.py`:

```python
import os

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'your_account_sid_here')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'your_auth_token_here')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+1234567890')
FRIEND_PHONE_NUMBER = os.environ.get('FRIEND_PHONE_NUMBER', '+1234567890')
```

Then set environment variables:

**macOS/Linux:**
```bash
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_PHONE_NUMBER="+15551234567"
export FRIEND_PHONE_NUMBER="+16171234567"
```

**Windows:**
```cmd
set TWILIO_ACCOUNT_SID=your_sid
set TWILIO_AUTH_TOKEN=your_token
```

## Alternative Weather APIs

The script uses wttr.in (free, no API key). Alternatives:

### OpenWeatherMap
- Free tier: 1000 calls/day
- Sign up: https://openweathermap.org/api

### WeatherAPI.com
- Free tier: 1M calls/month
- Sign up: https://www.weatherapi.com/

## Customization

### Change Message Timing
Edit the cron schedule or GitHub Actions schedule.

### Add More Jokes
Edit the `generate_playful_message()` function to add your own jokes to the arrays.

### Different Locations
Update the latitude/longitude constants at the top of the script.

### Message Format
Modify the `generate_playful_message()` function to change structure, add emojis, etc.

## Troubleshooting

**"Module not found" error:**
```bash
pip install requests twilio
```

**Twilio authentication error:**
- Double-check Account SID and Auth Token
- Ensure no extra spaces in credentials

**Message not sending:**
- Verify phone numbers include country code (+1 for US)
- For trial accounts, verify recipient's number in Twilio Console

**Cron job not running:**
```bash
# Check cron is running
ps aux | grep cron

# View cron logs (macOS)
log show --predicate 'process == "cron"' --last 1h

# View cron logs (Linux)
grep CRON /var/log/syslog
```

## Cost Estimate

- **Twilio SMS:** $0.0075 per message sent
- **Daily for one year:** $0.0075 × 365 = ~$2.74/year
- **Free tier credit:** $15 = ~5.5 years of daily messages

## Support

- Twilio Docs: https://www.twilio.com/docs
- wttr.in: https://github.com/chubin/wttr.in
