import requests
from datetime import datetime
import pytz

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    # 1. Получаем координаты города (нужны для AQI и UV)
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_res = requests.get(geo_url).json()
    lat, lon = geo_res[0]['lat'], geo_res[0]['lon']

    # 2. Получаем основную погоду
    w_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    w_res = requests.get(w_url).json()

    # 3. Получаем Качество воздуха (AQI)
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    aqi_res = requests.get(aqi_url).json()
    aqi_val = aqi_res['list'][0]['main']['aqi']
    aqi_desc = {1: "Excellent ✅", 2: "Fair 🟢", 3: "Moderate 🟡", 4: "Poor 🟠", 5: "Dangerous 🔴"}[aqi_val]

    # Данные для сообщения
    temp = round(w_res['main']['temp'])
    feels_like = round(w_res['main']['feels_like'])
    desc = w_res['weather'][0]['description'].capitalize()
    hum = w_res['main']['humidity']
    wind = w_res['wind']['speed']

    # Логика советов
    advice = "Wear a warm coat! 🧥" if feels_like < 10 else "Light clothes are fine. 👕"
    if aqi_val >= 4: advice += " Air quality is poor, avoid long runs outside. 😷"

    # Время
    tz_ny = pytz.timezone('America/New_York')
    time_ny = datetime.now(tz_ny).strftime("%I:%M %p")

    payload = {
        "embeds": [{
            "title": "🏙️ NYC Premium Weather Report",
            "description": f"Update for **{time_ny}**",
            "color": 3066993,
            "fields": [
                {"name": "🌡️ Temp / Feels", "value": f"**{temp}°C** / **{feels_like}°C**", "inline": True},
                {"name": "☁️ Sky", "value": f"{desc}", "inline": True},
                {"name": "💨 Wind", "value": f"{wind} m/s", "inline": True},
                {"name": "💧 Humidity", "value": f"{hum}%", "inline": True},
                {"name": "🍃 Air Quality", "value": f"**{aqi_desc}**", "inline": True},
                {"name": "🧥 Style Guide", "value": f"**{advice}**", "inline": False}
            ],
            "footer": {"text": "All-in-one NYC Assistant"}
        }]
    }
    
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    send_weather()
