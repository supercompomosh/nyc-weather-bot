import requests
from datetime import datetime
import pytz

def get_weather_data():
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    # Запрос текущей погоды и прогноза (используем 5-дневный прогноз для данных на завтра)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    return res

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    data = get_weather_data()
    
    if data["cod"] != "200":
        print("Error fetching data")
        return

    # Данные на сейчас (первый элемент списка)
    current = data['list'][0]
    temp = round(current['main']['temp'])
    desc = current['weather'][0]['description'].capitalize()
    
    # Данные на завтра (индекс 8 — это примерно +24 часа от текущего момента)
    tomorrow = data['list'][8]
    temp_tomorrow = round(tomorrow['main']['temp'])
    desc_tomorrow = tomorrow['weather'][0]['description']

    # Выбор иконки
    icon = "☀️" if "clear" in desc.lower() else "☁️"
    if "rain" in desc.lower(): icon = "🌧️"
    if "snow" in desc.lower(): icon = "❄️"

    # Время в Нью-Йорке
    tz_ny = pytz.timezone('America/New_York')
    time_ny = datetime.now(tz_ny).strftime("%I:%M %p")

    # Совет по одежде
    advice = "Dress warmly! 🧥" if temp < 10 else "Light clothes are fine. 👕"
    if "rain" in desc.lower(): advice += " And don't forget an umbrella! ☂️"

    payload = {
        "embeds": [{
            "title": f"{icon} Daily NYC Weather Report",
            "description": f"Good morning! Here is your update for **{time_ny}** (NYC Time).",
            "color": 16750848, # Оранжевый цвет
            "fields": [
                {"name": "Current Temp", "value": f"**{temp}°C**", "inline": True},
                {"name": "Condition", "value": f"{desc}", "inline": True},
                {"name": "Tomorrow", "value": f"**{temp_tomorrow}°C**, {desc_tomorrow}", "inline": False},
                {"name": "Style Guide", "value": f"💡 {advice}", "inline": False}
            ],
            "footer": {"text": "Powered by NYC AI Station"},
            "thumbnail": {"url": "https://i.imgur.com/w919WvY.png"} # Иконка города
        }]
    }
    
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    send_weather()
