import requests
from datetime import datetime
import pytz

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    
    if res["cod"] != "200": return

    # Текущие данные
    curr = res['list'][0]
    temp = round(curr['main']['temp'])
    feels_like = round(curr['main']['feels_like'])
    desc = curr['weather'][0]['description'].capitalize()
    hum = curr['main']['humidity']
    wind = curr['wind']['speed']
    
    # Завтра
    tom = res['list'][8]
    temp_tom = round(tom['main']['temp'])

    # Логика советов (Style Guide)
    if feels_like < 0:
        advice = "It's freezing! Heavy parka, thermal wear, and a scarf are a must. ❄️🧣"
    elif feels_like < 10:
        advice = "Chilly morning. A warm coat or a down jacket is recommended. 🧥"
    elif feels_like < 20:
        advice = "Mild weather. A light jacket, trench coat, or hoodie is perfect. 🧥👟"
    else:
        advice = "Warm day! T-shirt and light pants are enough. 👕🕶️"

    if "rain" in desc.lower():
        advice += " Don't forget your umbrella or a raincoat! ☂️"

    # Время
    tz_ny = pytz.timezone('America/New_York')
    time_ny = datetime.now(tz_ny).strftime("%I:%M %p")

    payload = {
        "embeds": [{
            "title": "🏙️ NYC Daily Style & Weather",
            "description": f"Update for **{time_ny}** in New York",
            "color": 3447003,
            "fields": [
                {"name": "🌡️ Temp", "value": f"**{temp}°C**", "inline": True},
                {"name": "🤔 Feels Like", "value": f"**{feels_like}°C**", "inline": True},
                {"name": "☁️ Sky", "value": f"{desc}", "inline": True},
                {"name": "💧 Humidity", "value": f"{hum}%", "inline": True},
                {"name": "💨 Wind", "value": f"{wind} m/s", "inline": True},
                {"name": "📅 Tomorrow", "value": f"Around **{temp_tom}°C**", "inline": True},
                {"name": "🧥 What to wear today?", "value": f"**{advice}**", "inline": False}
            ],
            "footer": {"text": "Your personal NYC assistant"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    send_weather()
