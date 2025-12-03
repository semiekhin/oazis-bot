"""
Загрузка данных из JSON и текстовых файлов.
Поддержка мультиобъектной структуры OAZIS.
"""

import json
import os
from typing import Dict, Any, List, Optional

from config.settings import (
    DATA_DIR,
    CONFIG_DIR,
    OBJECTS_DIR,
    INSTRUCTIONS_PATH,
    get_object_data_path,
)


def load_json_file(path: str) -> Optional[Any]:
    """Загружает JSON файл."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[DATA] File not found: {path}")
    except json.JSONDecodeError as e:
        print(f"[DATA] JSON parse error in {path}: {e}")
    except Exception as e:
        print(f"[DATA] Error loading {path}: {e}")
    return None


def load_text_file(path: str, default: str = "") -> str:
    """Загружает текстовый файл."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[DATA] File not found: {path}")
    except Exception as e:
        print(f"[DATA] Error loading {path}: {e}")
    return default


# ====== Загрузка данных объекта ======

def load_object_finance(city_id: str, object_id: str) -> Optional[Dict[str, Any]]:
    """Загружает финансовые данные объекта."""
    path = os.path.join(get_object_data_path(city_id, object_id), "finance.json")
    return load_json_file(path)


def load_object_knowledge(city_id: str, object_id: str) -> str:
    """Загружает базу знаний объекта."""
    path = os.path.join(get_object_data_path(city_id, object_id), "knowledge.txt")
    return load_text_file(path)


def load_object_text(city_id: str, object_id: str, filename: str) -> str:
    """Загружает текстовый файл объекта."""
    path = os.path.join(get_object_data_path(city_id, object_id), filename)
    return load_text_file(path)


# ====== Совместимость со старым кодом ======

def load_finance() -> Optional[Dict[str, Any]]:
    """
    Загружает финансы текущего/дефолтного объекта.
    Для совместимости со старым кодом — загружает RIZALTA.
    """
    return load_object_finance("altai", "rizalta")


def get_finance_defaults(finance: Dict[str, Any]) -> Dict[str, Any]:
    """Возвращает дефолтные параметры из finance."""
    return finance.get("defaults", {}) or {}


def get_finance_units(finance: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Возвращает список юнитов из finance."""
    return finance.get("units", []) or []


def get_min_lot(finance: Dict[str, Any]) -> Dict[str, Any]:
    """Возвращает минимальный лот из finance."""
    return finance.get("min_lot", {}) or {}


def get_installment_programs(finance: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Возвращает программы рассрочки."""
    return finance.get("installment_programs", []) or []


def get_mortgage_programs(finance: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Возвращает ипотечные программы."""
    return finance.get("mortgage_programs", []) or []


def get_investment_scenarios(finance: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Возвращает инвестиционные сценарии."""
    return finance.get("investment_scenarios", []) or []


# ====== Загрузка инструкций ======

def load_knowledge_base() -> str:
    """Загружает базу знаний для AI (RIZALTA по умолчанию)."""
    return load_object_knowledge("altai", "rizalta")


def load_instructions() -> str:
    """Загружает инструкции для AI."""
    base = load_text_file(INSTRUCTIONS_PATH)
    
    if not base:
        base = (
            "Ты — онлайн-консультант агентства недвижимости OAZIS. "
            "Помогаешь клиентам выбрать курортную недвижимость. "
            "Отвечаешь по-русски, дружелюбно и профессионально."
        )
    
    knowledge = load_knowledge_base()
    if knowledge:
        return f"{base}\n\n{'='*60}\nБАЗА ЗНАНИЙ:\n{'='*60}\n\n{knowledge}"
    
    return base


def load_why_rizalta_text() -> str:
    """Загружает текст 'Почему RIZALTA'."""
    return load_object_text("altai", "rizalta", "text_why_rizalta.md")
