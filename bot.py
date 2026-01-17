import requests
from datetime import datetime
import pytz

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    # Получаем данные (прогноз включает и текущую погоду)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    
    if res["cod"] != "200":
        print("Error")
        return

    # Данные НА СЕЙЧАС
    curr = res['list'][0]
    temp = round(curr['main']['temp'])
    desc = curr['weather'][0]['description'].capitalize()
    hum = curr['main']['humidity']
    wind = curr['wind']['speed']
    
    # Данные НА ЗАВТРА
    tomorrow = res['list'][8]
    temp_tom = round(tomorrow['main']['temp'])
    desc_tom = tomorrow['weather'][0]['description']

    # Время в Нью-Йорке
    tz_ny = pytz.timezone('America/New_York')
    time_ny = datetime.now(tz_ny).strftime("%I:%M %p")

    # Формируем красивый Embed
    payload = {
        "embeds": [{
            "title": f"🗽 NYC Weather Station",
            "description": f"Update for **{time_ny}** (Local Time)",
            "color": 16750848,
            "fields": [
                {"name": "🌡 Temperature", "value": f"**{temp}°C**", "inline": True},
                {"name": "☁️ Condition", "value": f"{desc}", "inline": True},
                {"name": "💧 Humidity", "value": f"{hum}%", "inline": True},
                {"name": "💨 Wind Speed", "value": f"{wind} m/s", "inline": True},
                {"name": "📅 Tomorrow", "value": f"**{temp_tom}°C**, {desc_tom}", "inline": False},
                {"name": "💡 Advice", "value": f"{'Wear a warm coat!' if temp < 10 else 'Enjoy the day!'}", "inline": False}
            ],
            "footer": {"text": "Automatic Daily Report"}
        }]
    }
    
    requests.post(webhook_url, json=payload)
    print("Full report sent!")

if __name__ == "__main__":
    send_weather()
