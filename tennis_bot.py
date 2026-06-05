import requests
import re
from datetime import datetime

BOT_TOKEN = "8711575445:AAFA2iJ9ZAUR0Mz5hd2XAGxPrJ02QMgszKc"
CHAT_ID = "343523199"

notified = set()

def send_telegram(text):
    print("📤 Отправка...")
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram отправлено")
        else:
            print(f"❌ Ошибка: {r.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

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
                        send_telegram(f"🎾 {score} - Сет {set_num}: {player1} vs {player2}")
                        print(f"🔔 НАЙДЕНО: {score} в сете {set_num}")
                        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Бот запущен! Отслеживаю счета 5:6, 6:5, 6:6 по сетам.")
    send_telegram("🟢 Бот перезапущен и начал мониторинг счетов 5:6, 6:5 и 6:6!")
    check()
