"""Функции для отправки ЗАКОДИРОВАННЫХ (желательно)
архивов на другой сервер и сообщений в тг бот.
"""

import urllib.parse
import urllib.request

from src.utils import load_config

# Загружаем конфиг
config = load_config()

BOT_TOKEN = config["bot_token"]
CHAT_IDS = config["chat_ids"]

# Формируем настройки из конфига
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_msg(text, chat_id):
    """Отправляет сообщение в телеграм бота."""
    url = API_URL
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    urllib.request.urlopen(url, data)


def send_msgs(text, chat_ids=CHAT_IDS):
    """Отправляет сообщения всей команде в тг."""
    for chat_id in chat_ids:
        send_msg(text=text, chat_id=chat_id)
