"""
Настройки и константы бота OAZIS.
"""

import os
from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv('/opt/oazis/.env')
import json
from typing import List, Dict, Any

# ====== Пути ======
_THIS_FILE = os.path.abspath(__file__)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_THIS_FILE))

BASE_DIR = os.getenv("BOT_BASE_DIR", _PROJECT_ROOT)
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
OBJECTS_DIR = os.path.join(DATA_DIR, "objects")

# Файлы данных
OBJECTS_CONFIG_PATH = os.path.join(OBJECTS_DIR, "config.json")
INSTRUCTIONS_PATH = os.path.join(CONFIG_DIR, "instructions.txt")

# ====== Telegram ======
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TG_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Менеджеры (ID через запятую)
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID", "").strip()

def get_manager_ids() -> List[int]:
    """Возвращает список ID менеджеров для уведомлений."""
    if not MANAGER_CHAT_ID:
        return []
    return [int(id.strip()) for id in MANAGER_CHAT_ID.split(",") if id.strip()]

# ====== OpenAI ======
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

# ====== Email ======
MANAGER_EMAIL = os.getenv("MANAGER_EMAIL", "").strip()
BOT_EMAIL = os.getenv("BOT_EMAIL", "bot@oazis.ru")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mail.ru")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()

# ====== Загрузка объектов ======
def load_objects_config() -> Dict[str, Any]:
    """Загружает конфигурацию городов и объектов."""
    try:
        with open(OBJECTS_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[CONFIG] Error loading objects config: {e}")
        return {"cities": []}

def get_cities() -> List[Dict[str, Any]]:
    """Возвращает список городов."""
    config = load_objects_config()
    return config.get("cities", [])

def get_city_by_id(city_id: str) -> Dict[str, Any]:
    """Находит город по ID."""
    for city in get_cities():
        if city["id"] == city_id:
            return city
    return {}

def get_object_by_id(city_id: str, object_id: str) -> Dict[str, Any]:
    """Находит объект по ID города и объекта."""
    city = get_city_by_id(city_id)
    for obj in city.get("objects", []):
        if obj["id"] == object_id:
            return obj
    return {}

def get_object_data_path(city_id: str, object_id: str) -> str:
    """Возвращает путь к папке данных объекта."""
    return os.path.join(OBJECTS_DIR, city_id, object_id)

# ====== Клавиатуры ======
MAIN_MENU_BUTTONS = [
    ["🏢 Выбрать объект"],
    ["💬 Подобрать по запросу"],
    ["📞 Связаться с менеджером"],
]

def get_cities_buttons() -> List[List[str]]:
    """Генерирует кнопки городов."""
    cities = get_cities()
    buttons = []
    row = []
    for city in cities:
        btn_text = f"{city['icon']} {city['name']}"
        row.append(btn_text)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append(["🔙 Назад"])
    return buttons

def get_objects_buttons(city_id: str) -> List[List[str]]:
    """Генерирует кнопки объектов города."""
    city = get_city_by_id(city_id)
    buttons = []
    for obj in city.get("objects", []):
        status = " 🔜" if obj.get("status") == "coming_soon" else ""
        buttons.append([f"🏠 {obj['name']}{status}"])
    buttons.append(["🔙 Назад"])
    return buttons

# Кнопки для объекта (когда выбран конкретный ЖК)
OBJECT_MENU_BUTTONS = [
    ["📖 О проекте"],
    ["💰 Расчёты"],
    ["🎯 Подобрать лот"],
    ["📎 Получить планировки"],
    ["🔥 Записаться на показ"],
    ["🔙 К списку объектов"],
]

# Триггеры сброса состояния
MAIN_MENU_TRIGGER_TEXTS = [
    "🏢 Выбрать объект",
    "💬 Подобрать по запросу", 
    "📞 Связаться с менеджером",
    "🔙 Назад",
    "🔙 К списку объектов",
]

# Кнопки меню расчётов
CALCULATIONS_BUTTONS = [
    ["📊 Рентабельность/доходность"],
    ["💳 Рассрочка и ипотека"],
    ["🔙 Назад"],
]

UNIT_SELECT_BUTTONS = [
    ["A209", "B210", "A305"],
    ["🔙 Назад"],
]
