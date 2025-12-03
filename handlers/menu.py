"""
Обработчики меню и навигации OAZIS.
"""

from typing import Dict, Any

from config.settings import (
    MAIN_MENU_BUTTONS,
    OBJECT_MENU_BUTTONS,
    get_cities,
    get_city_by_id,
    get_cities_buttons,
    get_objects_buttons,
)
from models.state import (
    clear_user_state,
    clear_dialog_state,
    set_dialog_state,
    set_selected_city,
    set_selected_object,
    get_selected_city,
    get_selected_object,
    clear_selection,
    DialogStates,
)
from services.telegram import send_message, send_message_inline


async def handle_start(chat_id: int, text: str = "", user_info: Dict[str, Any] = None):
    """
    Обработка /start — приветствие и главное меню OAZIS.
    """
    clear_user_state(chat_id)
    
    welcome = (
        "👋 Добро пожаловать в <b>OAZIS</b>!\n\n"
        "Мы — агентство недвижимости, специализирующееся на курортных объектах.\n\n"
        "🏢 <b>Выбрать объект</b> — посмотреть ЖК по городам\n"
        "💬 <b>Подобрать по запросу</b> — расскажите свою ситуацию, и я подберу подходящий вариант\n"
        "📞 <b>Связаться с менеджером</b> — получить консультацию\n\n"
        "Выберите действие 👇"
    )
    
    await send_message(chat_id, welcome, with_keyboard=True, buttons=MAIN_MENU_BUTTONS)


async def handle_help(chat_id: int):
    """Обработка /help."""
    text = (
        "🆘 <b>Помощь по боту OAZIS</b>\n\n"
        "Я помогу вам найти идеальную недвижимость на курортах России.\n\n"
        "<b>Что я умею:</b>\n"
        "🏢 Показать объекты в разных городах\n"
        "💰 Рассчитать доходность и условия покупки\n"
        "🎯 Подобрать объект под ваш бюджет и цели\n"
        "📎 Отправить планировки\n"
        "📞 Записать на консультацию\n\n"
        "Напишите свой запрос или выберите действие в меню."
    )
    await send_message(chat_id, text, with_keyboard=True, buttons=MAIN_MENU_BUTTONS)


async def handle_back(chat_id: int):
    """Обработка кнопки Назад — контекстный возврат."""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if object_id:
        # Из меню объекта → к списку объектов города
        set_selected_object(chat_id, None)
        await handle_show_objects(chat_id, city_id)
    elif city_id:
        # Из списка объектов → к списку городов
        clear_selection(chat_id)
        await handle_show_cities(chat_id)
    else:
        # К главному меню
        clear_dialog_state(chat_id)
        await send_message(chat_id, "Главное меню:", with_keyboard=True, buttons=MAIN_MENU_BUTTONS)


async def handle_back_to_objects(chat_id: int):
    """Возврат к списку объектов текущего города."""
    city_id = get_selected_city(chat_id)
    set_selected_object(chat_id, None)
    clear_dialog_state(chat_id)
    
    if city_id:
        await handle_show_objects(chat_id, city_id)
    else:
        await handle_show_cities(chat_id)


# ====== Выбор города ======

async def handle_show_cities(chat_id: int):
    """Показывает список городов."""
    set_dialog_state(chat_id, DialogStates.CHOOSING_CITY)
    clear_selection(chat_id)
    
    text = (
        "🏙 <b>Выберите город</b>\n\n"
        "У нас есть объекты в следующих локациях:"
    )
    
    buttons = get_cities_buttons()
    await send_message(chat_id, text, with_keyboard=True, buttons=buttons)


async def handle_city_selected(chat_id: int, city_id: str):
    """Обработка выбора города."""
    city = get_city_by_id(city_id)
    if not city:
        await send_message(chat_id, "Город не найден.")
        return
    
    set_selected_city(chat_id, city_id)
    await handle_show_objects(chat_id, city_id)


# ====== Выбор объекта ======

async def handle_show_objects(chat_id: int, city_id: str):
    """Показывает список объектов в городе."""
    city = get_city_by_id(city_id)
    if not city:
        await handle_show_cities(chat_id)
        return
    
    set_dialog_state(chat_id, DialogStates.CHOOSING_OBJECT)
    
    objects_count = len(city.get("objects", []))
    active_count = len([o for o in city.get("objects", []) if o.get("status") == "active"])
    
    text = (
        f"{city['icon']} <b>{city['name']}</b>\n\n"
        f"Объектов: {objects_count}\n"
    )
    
    if active_count < objects_count:
        text += "🔜 — скоро в продаже\n"
    
    text += "\nВыберите объект:"
    
    buttons = get_objects_buttons(city_id)
    await send_message(chat_id, text, with_keyboard=True, buttons=buttons)


async def handle_object_selected(chat_id: int, city_id: str, object_id: str):
    """Обработка выбора объекта."""
    from config.settings import get_object_by_id
    
    obj = get_object_by_id(city_id, object_id)
    if not obj:
        await send_message(chat_id, "Объект не найден.")
        return
    
    if obj.get("status") == "coming_soon":
        await send_message(
            chat_id,
            f"🔜 <b>{obj['name']}</b>\n\n"
            "Этот объект скоро появится в продаже.\n"
            "Хотите узнать первым? Оставьте заявку, и мы свяжемся с вами!",
        )
        return
    
    set_selected_object(chat_id, object_id)
    set_dialog_state(chat_id, DialogStates.IN_OBJECT_MENU)
    
    city = get_city_by_id(city_id)
    
    text = (
        f"🏠 <b>{obj['name']}</b>\n"
        f"📍 {city['name']}\n\n"
        "Выберите, что вас интересует:"
    )
    
    await send_message(chat_id, text, with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)


# ====== Меню объекта (О проекте, Расчёты...) ======

async def handle_about_project(chat_id: int):
    """О проекте — для выбранного объекта."""
    from handlers.object_handlers import show_object_about
    await show_object_about(chat_id)


async def handle_calculations_menu(chat_id: int):
    """Расчёты — для выбранного объекта."""
    from handlers.object_handlers import show_object_calculations
    await show_object_calculations(chat_id)


# ====== AI консультация ======

async def handle_ai_consultation(chat_id: int):
    """Начало AI консультации."""
    set_dialog_state(chat_id, DialogStates.AI_CONSULTATION)
    
    text = (
        "💬 <b>Расскажите о себе</b>\n\n"
        "Опишите вашу ситуацию:\n"
        "• Цель покупки (инвестиция, для жизни, переезд)\n"
        "• Бюджет\n"
        "• Предпочтения по локации\n"
        "• Любые другие пожелания\n\n"
        "Я проанализирую и подберу подходящие варианты 🏠"
    )
    
    await send_message(chat_id, text, with_keyboard=True, buttons=[["🔙 Назад"]])


async def handle_contact_manager(chat_id: int):
    """Связь с менеджером."""
    from handlers.booking import handle_online_show_start
    await handle_online_show_start(chat_id)
