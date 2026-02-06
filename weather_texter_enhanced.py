#!/usr/bin/env python3
"""
Daily Weather Comparison Bot - Enhanced Version
Sends playful weather updates comparing Del Mar, CA to Boston, MA

Features:
- Environment variable support for credentials
- Better error handling and logging
- Configurable via command-line arguments
- Dry-run mode for testing
"""

import requests
import random
import os
import argparse
from datetime import datetime
from twilio.rest import Client

# ============= CONFIGURATION =============
# Read from environment variables (more secure) with fallbacks
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
FRIEND_PHONE_NUMBER = os.environ.get('FRIEND_PHONE_NUMBER', '')

# Locations
DEL_MAR_LAT = 32.9595
DEL_MAR_LON = -117.2653
BOSTON_LAT = 42.3601
BOSTON_LON = -71.0589


# ============= WEATHER FETCHING =============
def get_weather(lat, lon, location_name):
    """Fetch weather using wttr.in service (free, no API key)"""
    try:
        url = f"https://wttr.in/{lat},{lon}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data['current_condition'][0]
        today = data['weather'][0]
        
        return {
            'location': location_name,
            'temp': int(current['temp_F']),
            'condition': current['weatherDesc'][0]['value'],
            'high': int(today['maxtempF']),
            'low': int(today['mintempF']),
            'humidity': int(current['humidity']),
            'feels_like': int(current['FeelsLikeF'])
        }
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error fetching weather for {location_name}: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"❌ Error parsing weather data for {location_name}: {e}")
        return None


# ============= MESSAGE GENERATION =============
def generate_playful_message(delmar_weather, boston_weather):
    """Generate a playful comparison message with varied commentary"""
    
    temp_diff = delmar_weather['high'] - boston_weather['high']
    feels_like_diff = delmar_weather['feels_like'] - boston_weather['feels_like']
    
    # Playful opening lines
    openers = [
        "☀️ *California Weather Report* ☀️",
        "🌴 Greetings from paradise! 🌴",
        "📍 Live from the Best Coast:",
        "🏖️ Your daily dose of sunshine envy:",
        "☀️ Breaking news from Del Mar:",
        "🌊 Surf's up and so is the temperature!",
        "🎯 Your daily weather flex:",
    ]
    
    # Temperature comparisons based on severity
    if temp_diff > 45:
        temp_jokes = [
            f"It's a balmy {delmar_weather['high']}°F here while you're experiencing the arctic tundra at {boston_weather['high']}°F. That's a {temp_diff}° difference! 🥶❄️",
            f"We're absolutely SUFFERING at {delmar_weather['high']}°F. I know, I know... you've got it worse at {boston_weather['high']}°F. 😂",
            f"High of {delmar_weather['high']}°F here. You're at {boston_weather['high']}°F. Math says that's {temp_diff}° warmer, but who's counting? (Me. I'm counting.) 😎",
            f"Temperature check: Del Mar {delmar_weather['high']}°F ☀️ | Boston {boston_weather['high']}°F 🧊 | Difference: 'Why do you still live there?' degrees",
        ]
    elif temp_diff > 35:
        temp_jokes = [
            f"Del Mar: {delmar_weather['high']}°F ☀️ | Boston: {boston_weather['high']}°F 🥶 (only {temp_diff}° difference, totally not rubbing it in)",
            f"It's {temp_diff}° warmer here ({delmar_weather['high']}°F vs your {boston_weather['high']}°F). That's like... a whole different season! 🌞❄️",
            f"We hit {delmar_weather['high']}°F today. You're at {boston_weather['high']}°F. But I'm sure the cold builds character or something! 💪🥶",
        ]
    elif temp_diff > 25:
        temp_jokes = [
            f"Today's forecast: {delmar_weather['high']}°F in Del Mar, {boston_weather['high']}°F in Boston. Almost twins! (If one twin lives in paradise) 😏",
            f"High of {delmar_weather['high']}°F vs {boston_weather['high']}°F. See? Only {temp_diff}° apart. Basically neighbors! 🌴🧊",
        ]
    else:
        temp_jokes = [
            f"We're at {delmar_weather['high']}°F, you're at {boston_weather['high']}°F. Practically the same! 😅",
            f"Shockingly close today: {delmar_weather['high']}°F here, {boston_weather['high']}°F there. Only {temp_diff}° different!",
        ]
    
    # "Feels like" commentary
    feels_like_jokes = []
    if feels_like_diff > 40:
        feels_like_jokes.append(f"(Feels like {delmar_weather['feels_like']}°F here vs {boston_weather['feels_like']}°F there... wind chill is your nemesis!) 🌬️")
    
    # Weather condition jokes
    condition_jokes = []
    boston_condition_lower = boston_weather['condition'].lower()
    
    if 'snow' in boston_condition_lower:
        condition_jokes.extend([
            "I'd send you some sunshine but it doesn't ship well. ☀️📦",
            "Hope you're enjoying that 'winter wonderland' experience! I might hit the beach later. 🏖️",
            "Snow day for you, beach day for me? Life's wild! 🤷‍♂️⛄",
            "Remember when you said you 'love the seasons'? How's that going? ⛄❄️",
        ])
    elif 'rain' in boston_condition_lower or 'drizzle' in boston_condition_lower:
        condition_jokes.extend([
            "At least your cold is hydrated! 🌧️",
            "Nothing says February like cold rain in New England! 🌧️😬",
        ])
    elif 'cloud' in boston_condition_lower:
        condition_jokes.append("Cloudy with a chance of regret about living in New England? ☁️")
    
    delmar_condition_lower = delmar_weather['condition'].lower()
    if 'sunny' in delmar_condition_lower or 'clear' in delmar_condition_lower:
        condition_jokes.append("Not a cloud in the sky here! Debating between beach or pool. 😎☀️")
    elif 'partly' in delmar_condition_lower:
        condition_jokes.append("We've got a few clouds. It's basically suffering. 😅☁️")
    
    # Closing lines
    closers = [
        "\nThink of it as character building! 💪",
        "\nBut hey, fall foliage is pretty... in 8 months! 🍂",
        "\nYou chose this! Well, someone did. 😂",
        "\nSpring is only... *checks calendar* ...a few months away! 🌸",
        "\nAt least your heating bill keeps the economy going! 💸",
        "\nStay warm, buddy! ❄️ (I'll be wearing shorts)",
        "\nRemember: You can always visit! 🛫☀️",
        "\nOn the bright side... okay I got nothing. Stay strong! 💪",
        "\nJust remember: it's a dry cold! Oh wait... 🤔",
    ]
    
    # Assemble message
    message_parts = [
        random.choice(openers),
        "",
        random.choice(temp_jokes),
    ]
    
    if feels_like_jokes and random.random() > 0.5:  # 50% chance to include feels-like
        message_parts.append(random.choice(feels_like_jokes))
    
    if condition_jokes:
        message_parts.append(random.choice(condition_jokes))
    
    message_parts.append(random.choice(closers))
    
    return "\n".join(message_parts)


# ============= SMS SENDING =============
def send_sms(message, dry_run=False):
    """Send SMS via Twilio (or simulate in dry-run mode)"""
    
    if dry_run:
        print("🧪 DRY RUN MODE - Message NOT actually sent")
        return True
    
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, FRIEND_PHONE_NUMBER]):
        print("❌ Missing Twilio credentials. Set environment variables:")
        print("   TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, FRIEND_PHONE_NUMBER")
        return False
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message_obj = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=FRIEND_PHONE_NUMBER
        )
        
        print(f"✅ Message sent successfully!")
        print(f"   SID: {message_obj.sid}")
        print(f"   Status: {message_obj.status}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending SMS: {e}")
        return False


# ============= MAIN EXECUTION =============
def main():
    parser = argparse.ArgumentParser(description='Send daily weather comparison texts')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Generate message but do not send SMS')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output (for cron jobs)')
    args = parser.parse_args()
    
    if not args.quiet:
        print(f"🤖 Weather Comparison Bot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    # Fetch weather data
    if not args.quiet:
        print("📡 Fetching weather data...")
    
    delmar = get_weather(DEL_MAR_LAT, DEL_MAR_LON, "Del Mar, CA")
    boston = get_weather(BOSTON_LAT, BOSTON_LON, "Boston, MA")
    
    if not delmar or not boston:
        print("❌ Failed to fetch weather data")
        return 1
    
    if not args.quiet:
        print(f"   Del Mar: {delmar['high']}°F (feels like {delmar['feels_like']}°F) - {delmar['condition']}")
        print(f"   Boston: {boston['high']}°F (feels like {boston['feels_like']}°F) - {boston['condition']}")
        print()
    
    # Generate message
    message = generate_playful_message(delmar, boston)
    
    if not args.quiet:
        print("="*60)
        print("MESSAGE PREVIEW:")
        print("="*60)
        print(message)
        print("="*60)
        print()
    
    # Send SMS
    if not args.quiet:
        print("📱 Sending message...")
    
    success = send_sms(message, dry_run=args.dry_run)
    
    if args.quiet and not success:
        print(f"ERROR: Failed to send message at {datetime.now()}")
        return 1
    
    if not args.quiet:
        print("\n✅ Complete!")
    
    return 0


if __name__ == "__main__":
    exit(main())
