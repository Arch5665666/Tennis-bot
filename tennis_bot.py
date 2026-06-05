import requests
import re
import smtplib
from email.message import EmailMessage
from datetime import datetime

# ---------- НАСТРОЙКИ ----------
BOT_TOKEN = "8711575445:AAFA2iJ9ZAUR0Mz5hd2XAGxPrJ02QMgszKc"
CHAT_ID = "343523199"

# НАСТРОЙКИ ПОЧТЫ
EMAIL_ADDRESS = "Tennis.bet.66@yandex.ru"
EMAIL_PASSWORD = "Art1479632014twnniabet"  # НЕ обычный пароль, а пароль приложения!

notified = set()

# ---------- ОТПРАВКА В TELEGRAM ----------
def send_telegram(text):
    print("📤 Отправка в Telegram...")
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram отправлено")
        else:
            print(f"❌ Ошибка Telegram: {r.status_code}")
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")

# ---------- ОТПРАВКА НА ПОЧТУ ----------
def send_email(subject, body):
    print("📧 Отправка на почту...")
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        
        with smtplib.SMTP_SSL("smtp.yandex.ru", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Письмо отправлено")
    except Exception as e:
        print(f"❌ Ошибка почты: {e}")

# ---------- ОТПРАВКА ВО ВСЕ КАНАЛЫ ----------
def send_all(message):
    send_telegram(message)
    send_email("🎾 Теннис-бот: новое уведомление", message)

# ---------- ПРОВЕРКА САЙТА ----------
def check():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        html = requests.get("https://sportscore.com/tennis/?filter=live", headers=headers, timeout=15).text
        
        match_blocks = re.findall(r'<a href="/tennis/match/[^"]+"[^>]*>(.*?)</a>', html, re.DOTALL)
        
        for block in match_blocks:
            players = re.findall(r'<div class="mx-1 d-flex align-items-center">([^<]+)</div>', block)
            if len(players) < 2:
                continue
            
            player1 = players[0].strip()
            player2 = players[1].strip()
            
            sets = re.findall(r'<div class="tennis-set(?: is-current)?\s*">\s*<div class="tennis-set__side tennis-set__a[^>]*">(\d+)</div>\s*<div class="tennis-set__side tennis-set__b[^>]*">(\d+)</div>', block, re.DOTALL)
            
            for set_num, (s1, s2) in enumerate(sets, 1):
                score = f"{s1}:{s2}"
                if score in ("5:6", "6:5", "6:6"):
                    key = f"{player1}|{player2}|сет{set_num}|{score}"
                    
                    if key not in notified:
                        notified.add(key)
                        message = f"🎾 {score} - Сет {set_num}: {player1} vs {player2}"
                        send_all(message)
                        print(f"🔔 НАЙДЕНО: {score} в сете {set_num}")
                        
    except Exception as e:
        print(f"Ошибка: {e}")

# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    print("🚀 Бот запущен! Отслеживаю счета 5:6, 6:5, 6:6 по сетам.")
    send_all("🟢 Бот перезапущен и начал мониторинг счетов 5:6, 6:5 и 6:6!")
    check()
