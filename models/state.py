"""
Модели состояний диалогов пользователей.

Все состояния хранятся in-memory (в словарях).
При перезапуске бота состояния сбрасываются.
"""

from typing import Dict, Any, Optional

# ====== Состояния диалогов ======

DIALOG_STATE: Dict[int, Any] = {}
LAST_KNOWN_BUDGET: Dict[int, int] = {}
LAST_KNOWN_FORMAT: Dict[int, str] = {}
ONLINE_BOOKING_STATE: Dict[int, Dict[str, Any]] = {}

# ====== НОВОЕ: Выбранный город и объект ======
SELECTED_CITY: Dict[int, str] = {}      # chat_id -> city_id
SELECTED_OBJECT: Dict[int, str] = {}    # chat_id -> object_id


# ====== Константы состояний ======

class DialogStates:
    """Возможные состояния диалога."""
    
    # Навигация
    CHOOSING_CITY = "choosing_city"
    CHOOSING_OBJECT = "choosing_object"
    CHOOSING_PAYMENT = "choosing_payment"
    CHOOSING_ROOMS = "choosing_rooms"
    ASKING_NAME = "asking_name"
    ASKING_PHONE = "asking_phone"
    IN_OBJECT_MENU = "in_object_menu"
    
    # Подбор лота
    CHOOSE_UNIT_ASK_BUDGET = "choose_unit_ask_budget"
    CHOOSE_UNIT_ASK_FORMAT = "choose_unit_ask_format"
    AWAIT_BUDGET = "await_budget"
    AWAIT_FORMAT = "await_format"
    
    # Выбор юнита для расчётов
    CHOOSE_ROI_UNIT = "choose_roi_unit"
    CHOOSE_FINANCE_UNIT = "choose_finance_unit"
    CHOOSE_PLAN_UNIT = "choose_plan_unit"
    
    # Контакт для связи
    ASK_CONTACT_FOR_CALLBACK = "ask_contact_for_callback"
    
    # AI консультация
    AI_CONSULTATION = "ai_consultation"
    
    # Многошаговая запись на показ
    BOOKING_ASK_NAME = "ask_name"
    BOOKING_ASK_CONTACT = "ask_contact"
    BOOKING_ASK_TIME = "ask_time"


# ====== Функции управления состояниями ======

def clear_user_state(chat_id: int) -> None:
    """Полностью очищает все состояния пользователя."""
    DIALOG_STATE.pop(chat_id, None)
    LAST_KNOWN_BUDGET.pop(chat_id, None)
    LAST_KNOWN_FORMAT.pop(chat_id, None)
    ONLINE_BOOKING_STATE.pop(chat_id, None)
    SELECTED_CITY.pop(chat_id, None)
    SELECTED_OBJECT.pop(chat_id, None)


def get_dialog_state(chat_id: int) -> Optional[Any]:
    return DIALOG_STATE.get(chat_id)


def set_dialog_state(chat_id: int, state: Any) -> None:
    DIALOG_STATE[chat_id] = state


def clear_dialog_state(chat_id: int) -> None:
    DIALOG_STATE.pop(chat_id, None)


# ====== Город и объект ======

def set_selected_city(chat_id: int, city_id: str) -> None:
    SELECTED_CITY[chat_id] = city_id
    SELECTED_OBJECT.pop(chat_id, None)  # Сбрасываем объект при смене города


def get_selected_city(chat_id: int) -> Optional[str]:
    return SELECTED_CITY.get(chat_id)


def set_selected_object(chat_id: int, object_id: str) -> None:
    SELECTED_OBJECT[chat_id] = object_id


def get_selected_object(chat_id: int) -> Optional[str]:
    return SELECTED_OBJECT.get(chat_id)


def clear_selection(chat_id: int) -> None:
    """Сбрасывает выбор города и объекта."""
    SELECTED_CITY.pop(chat_id, None)
    SELECTED_OBJECT.pop(chat_id, None)


# ====== Бюджет и формат ======

def save_budget(chat_id: int, budget: int) -> None:
    LAST_KNOWN_BUDGET[chat_id] = budget


def get_budget(chat_id: int) -> Optional[int]:
    return LAST_KNOWN_BUDGET.get(chat_id)


def save_format(chat_id: int, pay_format: str) -> None:
    LAST_KNOWN_FORMAT[chat_id] = pay_format


def get_format(chat_id: int) -> Optional[str]:
    return LAST_KNOWN_FORMAT.get(chat_id)


# ====== Многошаговая запись на показ ======

def start_booking(chat_id: int) -> None:
    ONLINE_BOOKING_STATE[chat_id] = {"stage": DialogStates.BOOKING_ASK_NAME}


def get_booking_state(chat_id: int) -> Optional[Dict[str, Any]]:
    return ONLINE_BOOKING_STATE.get(chat_id)


def update_booking_state(chat_id: int, **kwargs) -> None:
    if chat_id in ONLINE_BOOKING_STATE:
        ONLINE_BOOKING_STATE[chat_id].update(kwargs)


def clear_booking_state(chat_id: int) -> None:
    ONLINE_BOOKING_STATE.pop(chat_id, None)


def is_in_booking_flow(chat_id: int) -> bool:
    return chat_id in ONLINE_BOOKING_STATE
