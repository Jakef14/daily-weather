#!/usr/bin/env python3
"""
Daily Weather Comparison Bot
Sends playful weather updates comparing Del Mar, CA to Boston, MA
"""

import os
import requests
import random
from datetime import datetime
from twilio.rest import Client

# ============= CONFIGURATION =============
# Twilio credentials (get from https://www.twilio.com/console)

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
FRIEND_PHONE_NUMBER = os.environ.get('FRIEND_PHONE_NUMBER', '')

# Alternative: Use OpenWeatherMap, WeatherAPI.com, or similar
DEL_MAR_LAT = 32.9595
DEL_MAR_LON = -117.2653
BOSTON_LAT = 42.3601
BOSTON_LON = -71.0589


# ============= WEATHER FETCHING =============
def weather_code_to_text(code):
    mapping = {
        0: "Clear",
        1: "Mostly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light Drizzle",
        53: "Drizzle",
        55: "Heavy Drizzle",
        61: "Light Rain",
        63: "Rain",
        65: "Heavy Rain",
        71: "Light Snow",
        73: "Snow",
        75: "Heavy Snow",
        95: "Thunderstorm",
    }
    return mapping.get(code, "Unknown")

def get_weather(lat, lon, location_name):
    """Fetch weather using Open-Meteo (free, no API key, reliable)"""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}"
            f"&longitude={lon}"
            "&current_weather=true"
            "&daily=temperature_2m_max,temperature_2m_min"
            "&temperature_unit=fahrenheit"
            "&timezone=auto"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_weather"]
        daily = data["daily"]

        return {
            "location": location_name,
            "temp": int(round(current["temperature"])),
            "condition": weather_code_to_text(current["weathercode"]),
            "high": int(round(daily["temperature_2m_max"][0])),
            "low": int(round(daily["temperature_2m_min"][0])),
        }

    except Exception as e:
        print(f"Error fetching weather for {location_name}: {e}")
        return None


# ============= MESSAGE GENERATION =============
def generate_playful_message(delmar_weather, boston_weather):
    """Generate a playful comparison message"""
    
    temp_diff = delmar_weather['high'] - boston_weather['high']
    
    # Playful opening lines
    openers = [
        "☀️ *California Weather Report* ☀️",
        "🌴 Greetings from paradise! 🌴",
        "📍 Live from the Best Coast:",
        "🏖️ Your daily dose of sunshine envy:",
        "☀️ Breaking news from Del Mar:",
    ]
    
    # Temperature comparisons
    if temp_diff > 40:
        temp_jokes = [
            f"It's a balmy {delmar_weather['high']}°F here while you're freezing at {boston_weather['high']}°F. That's a {temp_diff}° difference! 🥶",
            f"Currently {delmar_weather['high']}°F in Del Mar. Meanwhile you're experiencing a tropical {boston_weather['high']}°F. Practically twins! 😂",
            f"We're suffering through {delmar_weather['high']}°F weather. How are you managing in that heat wave of {boston_weather['high']}°F? 🏖️❄️",
        ]
    elif temp_diff > 30:
        temp_jokes = [
            f"Del Mar: {delmar_weather['high']}°F ☀️ | Boston: {boston_weather['high']}°F 🥶 (but who's counting the {temp_diff}° difference?)",
            f"It's only {temp_diff}° warmer here ({delmar_weather['high']}°F vs your {boston_weather['high']}°F). Barely noticeable! 😎",
        ]
    else:
        temp_jokes = [
            f"We're at {delmar_weather['high']}°F, you're at {boston_weather['high']}°F. Almost the same! 😏",
            f"Today's high: {delmar_weather['high']}°F in Del Mar, {boston_weather['high']}°F in Boston. See? Not that different! (Okay, {temp_diff}° different) 🌞",
        ]
    
    # Weather condition jokes
    condition_jokes = []
    if 'snow' in boston_weather['condition'].lower():
        condition_jokes.extend([
            "I'd send you some sunshine but it doesn't ship well. ☀️📦",
            "Hope you're enjoying that 'winter wonderland' experience! Meanwhile, I might go to the beach. 🏖️",
            "Snow day for you, beach day for me? 🤷‍♂️",
        ])
    elif 'rain' in boston_weather['condition'].lower():
        condition_jokes.extend([
            "At least it's a wet cold instead of a dry cold, right? 😅",
            "Nothing says February like rain in New England! 🌧️",
        ])
    
    if 'sunny' in delmar_weather['condition'].lower() or 'clear' in delmar_weather['condition'].lower():
        condition_jokes.append("Not a cloud in the sky here! 😎☀️")
    
    # Closing lines
    closers = [
        "\nThink of it as character building! 💪",
        "\nBut hey, fall foliage is nice... in 8 months! 🍂",
        "\nYou chose this! 😂",
        "\nSpring is only... *checks calendar* ...a while away! 🌸",
        "\nAt least your heating bill is keeping someone employed! 💸",
        "\nRemember: it's a dry cold! Oh wait... 🤔",
    ]
    
    # Assemble message
    message_parts = [
        random.choice(openers),
        "",
        random.choice(temp_jokes),
    ]
    
    if condition_jokes:
        message_parts.append(random.choice(condition_jokes))
    
    message_parts.append(random.choice(closers))
    
    return "\n".join(message_parts)


# ============= SMS SENDING =============
def send_sms(message):
    """Send SMS via Twilio"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message_obj = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=FRIEND_PHONE_NUMBER
        )
        
        print(f"✅ Message sent! SID: {message_obj.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending SMS: {e}")
        return False


# ============= MAIN EXECUTION =============
def main():
    print(f"🤖 Weather Comparison Bot Starting - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch weather data
    print("📡 Fetching Del Mar weather...")
    delmar = get_weather(DEL_MAR_LAT, DEL_MAR_LON, "Del Mar, CA")
    
    print("📡 Fetching Boston weather...")
    boston = get_weather(BOSTON_LAT, BOSTON_LON, "Boston, MA")
    
    if not delmar or not boston:
        print("❌ Failed to fetch weather data")
        return
    
    # Generate message
    print("✍️  Generating playful message...")
    message = generate_playful_message(delmar, boston)
    
    print("\n" + "="*50)
    print("MESSAGE PREVIEW:")
    print("="*50)
    print(message)
    print("="*50 + "\n")
    
    # Send SMS
    print("📱 Sending SMS...")
    send_sms(message)
    
    print("✅ Done!")


if __name__ == "__main__":
    main()
