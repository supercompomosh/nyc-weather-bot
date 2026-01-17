import requests
from datetime import datetime

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    
    if "main" not in res:
        print("Error fetching weather")
        return

    temp = round(res['main']['temp'])
    feels_like = round(res['main']['feels_like'])
    desc = res['weather'][0]['description'].capitalize()
    humidity = res['main']['humidity']
    wind = res['wind']['speed']

    # Логика советов
    if temp < 5:
        advice = "It's freezing! Wear a warm coat, hat, and gloves. 🧣"
    elif temp < 15:
        advice = "Chilly day. A light jacket or hoodie should be fine. 🧥"
    else:
        advice = "Great weather! Enjoy your walk in the city. 👕"

    # Красивое оформление (Embed)
    payload = {
        "embeds": [{
            "title": f"🌤 Weather Report: {city}",
            "color": 3447003, # Синий цвет
            "fields": [
                {"name": "Temperature", "value": f"**{temp}°C** (Feels like {feels_like}°C)", "inline": True},
                {"name": "Condition", "value": f"**{desc}**", "inline": True},
                {"name": "Humidity", "value": f"{humidity}%", "inline": True},
                {"name": "Wind Speed", "value": f"{wind} m/s", "inline": True},
                {"name": "What to wear?", "value": f"💡 {advice}", "inline": False}
            ],
            "footer": {"text": "NYC Daily Service | Automatic Update"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    requests.post(webhook_url, json=payload)
    print("Beautiful report sent!")

if __name__ == "__main__":
    send_weather()
