import requests
from datetime import datetime

BOT_TOKEN = "8711575445:AAFA2iJ9ZAUR0Mz5hd2XAGxPrJ02QMgszKc"
CHAT_ID = "343523199"

def send_telegram(text):
    print(f"📤 Отправка: {text[:50]}...")
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram отправлено")
        else:
            print(f"❌ Ошибка: {r.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Бот запущен на GitHub Actions!")
    send_telegram("🟢 Бот запущен! Отслеживаю счета 5:6, 6:5 и 6:6.")
    print("✅ Проверка завершена")
