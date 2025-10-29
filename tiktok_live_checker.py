import os
import time
import requests
from telegram import Bot

# === Настройки из переменных окружения ===
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME", "ef.sane")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # сек между проверками

bot = Bot(token=TELEGRAM_TOKEN)


def notify(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"[OK] Сообщение отправлено: {message}")
    except Exception as e:
        print(f"[ERR] Ошибка отправки: {e}")


def is_live(username):
    """Проверяем, в эфире ли пользователь TikTok"""
    try:
        url = f"https://www.tiktok.com/@{username}/live"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        return '"isLive":true' in response.text
    except Exception as e:
        print(f"[ERR] Ошибка проверки: {e}")
        return False


def main():
    print("✅ Бот запущен. Проверяю эфиры TikTok...")
    notify(f"✅ Бот активен. Проверяю эфир @{TIKTOK_USERNAME}...")

    was_live = False

    while True:
        live = is_live(TIKTOK_USERNAME)
        if live and not was_live:
            notify(f"🎥 Стрим у @{TIKTOK_USERNAME} начался!\nhttps://www.tiktok.com/@{TIKTOK_USERNAME}/live")
            was_live = True
        elif not live and was_live:
            notify(f"🔴 Стрим @{TIKTOK_USERNAME} завершён.")
            was_live = False
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
