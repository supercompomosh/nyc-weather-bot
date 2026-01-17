import requests
from datetime import datetime
import pytz

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    # 1. Получаем координаты
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_res = requests.get(geo_url).json()
    lat, lon = geo_res[0]['lat'], geo_res[0]['lon']

    # 2. Получаем текущую погоду и УФ-индекс
    # (У OpenWeatherMap УФ-индекс входит в One Call или запрашивается отдельно, 
    # но в базовом API мы берем данные о погоде и загрязнении)
    w_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    w_res = requests.get(w_url).json()

    # 3. Качество воздуха (AQI)
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    aqi_res = requests.get(aqi_url).json()
    aqi_val = aqi_res['list'][0]['main']['aqi']
    aqi_desc = {1: "Excellent ✅", 2: "Fair 🟢", 3: "Moderate 🟡", 4: "Poor 🟠", 5: "Dangerous 🔴"}[aqi_val]

    temp = round(w_res['main']['temp'])
    feels_like = round(w_res['main']['feels_like'])
    desc = w_res['weather'][0]['description'].capitalize()
    hum = w_res['main']['humidity']
    wind = w_res['wind']['speed']

    # Расширенная логика советов по одежде
    if feels_like < 0:
        style_advice = "Heavy winter coat, thermal layers, and gloves. It's freezing! ❄️"
    elif feels_like < 10:
        style_advice = "A warm wool coat or down jacket. Don't forget a scarf. 🧥"
    elif feels_like < 18:
        style_advice = "Light jacket, denim, or a trench coat. Perfect layered look. 🧥👟"
    else:
        style_advice = "T-shirt and light trousers. Enjoy the warmth! 👕"

    if "rain" in desc.lower():
        style_advice += " + Waterproof shoes and an umbrella! ☂️"

    # Время в Нью-Йорке
    tz_ny = pytz.timezone('America/New_York')
    time_ny = datetime.now(tz_ny).strftime("%I:%M %p")

    payload = {
        "embeds": [{
            "title": "🏙️ NYC Style & Weather",
            "description": f"Daily update for New Yorkers | **{time_ny}**",
            "color": 15418782, # Стильный золотисто-оранжевый
            "fields": [
                {"name": "🌡️ Temperature", "value": f"**{temp}°C** (Feels like {feels_like}°C)", "inline": False},
                {"name": "🌤️ Sky Condition", "value": f"{desc}", "inline": True},
                {"name": "💨 Wind", "value": f"{wind} m/s", "inline": True},
                {"name": "🍃 Air Quality", "value": f"{aqi_desc}", "inline": True},
                {"name": "🧥 Style Guide", "value": f"**{style_advice}**", "inline": False}
            ],
            "footer": {"text": "NYC Style Station • Stay Sharp, Stay Ready"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    send_weather()
