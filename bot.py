import requests
from datetime import datetime

# --- ВАШИ НАСТРОЙКИ ---
# Ссылку на вебхук я уже добавил
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"

# ВСТАВЬТЕ СВОЙ API КЛЮЧ НИЖЕ (между кавычками)
WEATHER_API_KEY = "ВАШ_API_КЛЮЧ_ЗДЕСЬ"

CITY = "New York"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    res = requests.get(url).json()
    
    temp = round(res['main']['temp'])
    desc = res['weather'][0]['description'].capitalize()
    
    # Логика советов (Pro Tip)
    advice = "Have a great day in the city!"
    if "rain" in desc.lower():
        advice = "Grab an umbrella, it's going to be rainy! ☔"
    elif temp < 5:
        advice = "Chilly day! Don't forget your coat. 🧥"
    
    return temp, desc, advice

def send_to_discord():
    temp, desc, advice = get_weather()
    
    # Красивое оформление для Discord
    payload = {
        "embeds": [{
            "title": f"📍 Daily Forecast: {CITY}",
            "color": 3447003, # Красивый синий цвет
            "fields": [
                {"name": "Temperature", "value": f"**{temp}°C**", "inline": True},
                {"name": "Condition", "value": f"**{desc}**", "inline": True},
                {"name": "Pro Tip", "value": advice, "inline": False}
            ],
            "footer": {"text": "NYC Weather Service | Verified Updates"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Success! Check your Discord channel.")
    else:
        print(f"Error: {response.status_code}")

# Запуск
send_to_discord()
