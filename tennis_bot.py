import requests

BOT_TOKEN = "8711575445:AAFA2iJ9ZAUR0Mz5hd2XAGxPrJ02QMgszKc"
CHAT_ID = "343523199"

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print("✅ Telegram")
    except Exception as e:
        print(f"❌ {e}")

def check():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get("https://sportscore.com/tennis/?filter=live", headers=headers, timeout=15).text
        
        if '5:6' in html or '6:5' in html:
            send_telegram("🎾 Найден счёт 5:6 или 6:5 на SportScore!")
            print("Найден счёт!")
        else:
            print("Ничего не найдено")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
