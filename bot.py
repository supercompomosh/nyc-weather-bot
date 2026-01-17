import requests

def send_weather():
    webhook_url = "https://discord.com/api/webhooks/1461880415060103229/VQYgZcfN_ql1q7g6b6qSdo1Sv1oT8dM0W0iQzPK1xnFDHLk7aUWrs93_LKsPy-SYdpsp"
    api_key = "c0bd6d7ddeab510249e24bc31bf6de61"
    city = "New York"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    # ПРОВЕРКА ОШИБОК
    if response.status_code != 200:
        error_msg = data.get('message', 'Unknown error')
        print(f"API Error: {error_msg}")
        # Отправляем тех. сообщение в Дискорд, чтобы вы знали об ошибке
        requests.post(webhook_url, json={"content": f"⚠️ Weather Bot Error: {error_msg}. (Check if your API key is active yet!)"})
        return

    # Если всё хорошо, берем данные
    temp = round(data['main']['temp'])
    desc = data['weather'][0]['description']
    
    payload = {
        "content": f"🗽 **NYC Weather Update**: {temp}°C, {desc}."
    }
    
    requests.post(webhook_url, json=payload)
    print("Success!")

if __name__ == "__main__":
    send_weather()
