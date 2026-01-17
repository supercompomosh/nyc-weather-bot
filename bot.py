import requests
from datetime import datetime
import pytz

def send_reports():
    # --- НАСТРОЙКИ ---
    tg_token = "8544880820:AAH3dSWrP8kVQZ2tXKnOYzUBSDbjZxhN83M" 
    tg_chat_id = "@MyNYCChannel"
    discord_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    # 1. Получаем данные (Погода + Гео)
    try:
        geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}").json()
        lat, lon = geo[0]['lat'], geo[0]['lon']
        
        w = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric").json()
        aqi_res = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}").json()
        
        temp = round(w['main']['temp'])
        feels = round(w['main']['feels_like'])
        desc = w['weather'][0]['description'].capitalize()
        hum = w['main']['humidity']
        wind = w['wind']['speed']
        aqi_val = aqi_res['list'][0]['main']['aqi']
        aqi_desc = {1: "Excellent ✅", 2: "Fair 🟢", 3: "Moderate 🟡", 4: "Poor 🟠", 5: "Dangerous 🔴"}[aqi_val]
        
        # Совет по стилю
        if feels < 5:
            advice = "Heavy winter coat & scarf. It's freezing! ❄️"
        elif feels < 15:
            advice = "Warm jacket or a light down coat. 🧥"
        elif feels < 22:
            advice = "Hoodie or a light trench coat. 🧥👟"
        else:
            advice = "T-shirt and shorts. Stay cool! 👕"

        time_ny = datetime.now(pytz.timezone('America/New_York')).strftime("%I:%M %p")

        # --- ОТПРАВКА В DISCORD ---
        discord_payload = {
            "embeds": [{
                "title": "🏙️ NYC Style & Weather",
                "description": f"Update for **{time_ny}**",
                "color": 15418782,
                "fields": [
                    {"name": "🌡️ Temp", "value": f"{temp}°C (Feels {feels}°C)", "inline": True},
                    {"name": "🍃 Air Quality", "value": f"{aqi_desc}", "inline": True},
                    {"name": "🧥 Style Guide", "value": f"**{advice}**", "inline": False}
                ],
                "footer": {"text": "NYC Style Station"}
            }]
        }
        requests.post(discord_url, json=discord_payload)

        # --- ОТПРАВКА В TELEGRAM ---
        tg_text = (
            f"🏙 <b>NYC Style & Weather</b>\n"
            f"<i>Local Time: {time_ny}</i>\n\n"
            f"🌡 <b>Temp:</b> {temp}°C (Feels like {feels}°C)\n"
            f"🌤 <b>Sky:</b> {desc}\n"
            f"🍃 <b>Air Quality:</b> {aqi_desc}\n"
            f"💨 <b>Wind:</b> {wind} m/s\n\n"
            f"🧥 <b>What to wear:</b>\n{advice}\n\n"
            f"🗽 Stay Sharp, New York!"
        )
        tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        requests.post(tg_url, data={"chat_id": tg_chat_id, "text": tg_text, "parse_mode": "HTML"})
        
        print("Success! Reports sent to Discord and Telegram.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_reports()
