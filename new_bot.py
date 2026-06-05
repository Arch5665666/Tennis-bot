import requests
from datetime import datetime

BOT_TOKEN = "8711575445:AAFA2iJ9ZAUR0Mz5hd2XAGxPrJ02QMgszKc"
CHAT_ID = "343523199"

def send_telegram(text):
    print(f"Попытка отправить: {text[:50]}...")
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram отправлено")
        else:
            print(f"❌ Ошибка HTTP: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")

if __name__ == "__main__":
    print("🚀 НОВЫЙ бот запущен на GitHub Actions!")
    send_telegram("🟢 НОВЫЙ бот запущен на GitHub Actions! Это тестовое сообщение.")
    print("✅ Проверка завершена")
