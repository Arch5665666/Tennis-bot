import requests
import json
import os
from datetime import datetime

BOT_TOKEN = "8711575445:AAFA2iJ9ZAUR0Mz5hd2XAGxPrJ02QMgszKc"
CHAT_ID = "343523199"

# Файл для хранения отправленных уведомлений
SEEN_FILE = "seen.json"

def load_seen():
    """Загружает список отправленных уведомлений"""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    """Сохраняет список отправленных уведомлений"""
    with open(SEEN_FILE, 'w') as f:
        json.dump(list(seen), f)

def send_telegram(text):
    """Отправляет сообщение в Telegram"""
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
    """Проверяет сайт на наличие счетов 5:6, 6:5, 6:6"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        html = requests.get("https://sportscore.com/tennis/?filter=live", headers=headers, timeout=15).text
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Проверка...")
        
        # Ищем все матчи
        import re
        match_blocks = re.findall(r'<a href="/tennis/match/[^"]+"[^>]*>(.*?)</a>', html, re.DOTALL)
        
        found_matches = []
        
        for block in match_blocks:
            # Ищем имена игроков
            players = re.findall(r'<div class="mx-1 d-flex align-items-center">([^<]+)</div>', block)
            if len(players) < 2:
                continue
            
            player1 = players[0].strip()
            player2 = players[1].strip()
            
            # Ищем сеты
            sets = re.findall(r'<div class="tennis-set(?: is-current)?\s*">\s*<div class="tennis-set__side tennis-set__a[^>]*">(\d+)</div>\s*<div class="tennis-set__side tennis-set__b[^>]*">(\d+)</div>', block, re.DOTALL)
            
            for set_num, (s1, s2) in enumerate(sets, 1):
                score = f"{s1}:{s2}"
                if score in ("5:6", "6:5", "6:6"):
                    key = f"{player1}|{player2}|сет{set_num}|{score}"
                    found_matches.append({
                        "key": key,
                        "player1": player1,
                        "player2": player2,
                        "set": set_num,
                        "score": score
                    })
        
        return found_matches
        
    except Exception as e:
        print(f"Ошибка проверки: {e}")
        return []

# ========== ОСНОВНОЙ ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 Бот запущен на GitHub Actions!")
    
    # Отправляем уведомление о запуске
    send_telegram("🟢 Бот запущен на GitHub Actions! Отслеживаю счета 5:6, 6:5 и 6:6 по сетам.")
    
    # Загружаем историю отправленных уведомлений
    seen = load_seen()
    
    # Проверяем сайт
    matches = check()
    
    # Отправляем уведомления о новых событиях
    for match in matches:
        if match["key"] not in seen:
            seen.add(match["key"])
            message = f"🎾 {match['score']} - Сет {match['set']}: {match['player1']} vs {match['player2']}"
            send_telegram(message)
            print(f"🔔 {message}")
    
    # Сохраняем историю
    save_seen(seen)
    
    print(f"✅ Проверка завершена. Найдено событий: {len(matches)}")
