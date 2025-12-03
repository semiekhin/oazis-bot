"""
Обработчики меню выбранного объекта
"""
from services.telegram import send_message, send_document
from services.data_loader import load_object_knowledge, load_object_finance
from models.state import get_selected_city, get_selected_object, set_dialog_state, DialogStates
from config.settings import get_object_by_id, get_city_by_id, OBJECT_MENU_BUTTONS, CALCULATIONS_BUTTONS, get_object_data_path
import os


async def show_object_about(chat_id: int):
    """Показать информацию о проекте"""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if not city_id or not object_id:
        await send_message(chat_id, "Сначала выберите объект", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
        return
    
    city = get_city_by_id(city_id)
    obj = get_object_by_id(city_id, object_id)
    
    if not obj:
        await send_message(chat_id, "Объект не найден", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
        return
    
    knowledge = load_object_knowledge(city_id, object_id)
    
    if knowledge:
        if len(knowledge) > 3500:
            knowledge = knowledge[:3500] + "\n\n... (продолжение по запросу)"
        
        city_name = city.get('name', city_id) if city else city_id
        obj_name = obj.get('name', object_id)
        
        message = f"📖 <b>{obj_name}</b> ({city_name})\n\n{knowledge}"
        await send_message(chat_id, message, with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
    else:
        await send_message(
            chat_id, 
            f"ℹ️ Информация о проекте {obj.get('name', object_id)} скоро будет добавлена.",
            with_keyboard=True,
            buttons=OBJECT_MENU_BUTTONS
        )


async def show_object_calculations(chat_id: int):
    """Показать меню расчётов (как в оригинале)"""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if not city_id or not object_id:
        await send_message(chat_id, "Сначала выберите объект", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
        return
    
    obj = get_object_by_id(city_id, object_id)
    obj_name = obj.get('name', object_id) if obj else object_id
    
    await send_message(
        chat_id,
        f"💰 <b>Финансовые расчёты — {obj_name}</b>\n\nВыберите, что вас интересует:",
        with_keyboard=True,
        buttons=CALCULATIONS_BUTTONS
    )


async def show_object_layouts(chat_id: int):
    """Отправить планировки объекта"""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if not city_id or not object_id:
        await send_message(chat_id, "Сначала выберите объект", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
        return
    
    obj = get_object_by_id(city_id, object_id)
    obj_name = obj.get('name', object_id) if obj else object_id
    
    layouts_dir = os.path.join(get_object_data_path(city_id, object_id), "layouts")
    
    if os.path.exists(layouts_dir):
        pdf_files = [f for f in os.listdir(layouts_dir) if f.endswith('.pdf')]
        if pdf_files:
            await send_message(chat_id, f"📎 Планировки <b>{obj_name}</b>:")
            for pdf_file in sorted(pdf_files)[:10]:
                pdf_path = os.path.join(layouts_dir, pdf_file)
                await send_document(chat_id, pdf_path)
            await send_message(chat_id, "Выберите действие:", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
            return
    
    await send_message(
        chat_id,
        f"ℹ️ Планировки для {obj_name} скоро будут добавлены.\n\nСвяжитесь с менеджером для получения актуальных планировок.",
        with_keyboard=True,
        buttons=OBJECT_MENU_BUTTONS
    )


async def start_lot_selection(chat_id: int):
    """Начать подбор лота"""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if not city_id or not object_id:
        await send_message(chat_id, "Сначала выберите объект", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
        return
    
    obj = get_object_by_id(city_id, object_id)
    obj_name = obj.get('name', object_id) if obj else object_id
    
    set_dialog_state(chat_id, DialogStates.CHOOSING_ROOMS)
    
    rooms_buttons = [
        ["Студия", "1-комн"],
        ["2-комн", "3-комн"],
        ["🔙 Назад"],
    ]
    
    await send_message(
        chat_id,
        f"🎯 Подбор лота в <b>{obj_name}</b>\n\nВыберите количество комнат:",
        with_keyboard=True,
        buttons=rooms_buttons
    )


async def start_showing_booking(chat_id: int):
    """Начать запись на показ"""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if not city_id or not object_id:
        await send_message(chat_id, "Сначала выберите объект", with_keyboard=True, buttons=OBJECT_MENU_BUTTONS)
        return
    
    obj = get_object_by_id(city_id, object_id)
    obj_name = obj.get('name', object_id) if obj else object_id
    
    set_dialog_state(chat_id, DialogStates.ASKING_NAME)
    
    await send_message(
        chat_id,
        f"🔥 Запись на показ <b>{obj_name}</b>\n\nКак вас зовут?",
        with_keyboard=True,
        buttons=[["🔙 Отмена"]]
    )


async def handle_choose_unit_for_roi(chat_id: int):
    """Выбор юнита для расчёта доходности."""
    unit_buttons = get_unit_buttons_for_object(chat_id)
    set_dialog_state(chat_id, DialogStates.CHOOSE_ROI_UNIT)
    
    await send_message(
        chat_id,
        "📊 <b>Рентабельность и доходность</b>\n\nВыберите апартамент для расчёта:",
        with_keyboard=True,
        buttons=unit_buttons,
    )


async def handle_choose_unit_for_finance(chat_id: int):
    """Выбор юнита для рассрочки/ипотеки."""
    unit_buttons = get_unit_buttons_for_object(chat_id)
    set_dialog_state(chat_id, DialogStates.CHOOSE_FINANCE_UNIT)
    
    await send_message(
        chat_id,
        "💳 <b>Рассрочка и ипотека</b>\n\nВыберите апартамент для расчёта:",
        with_keyboard=True,
        buttons=unit_buttons,
    )


def get_unit_buttons_for_object(chat_id: int) -> list:
    """Получить кнопки юнитов из finance.json выбранного объекта."""
    city_id = get_selected_city(chat_id)
    object_id = get_selected_object(chat_id)
    
    if not city_id or not object_id:
        return [["🔙 Назад"]]
    
    finance = load_object_finance(city_id, object_id)
    if not finance or "units" not in finance:
        return [["🔙 Назад"]]
    
    units = finance["units"]
    
    # Формируем кнопки с площадью: "27.91 м²"
    unit_buttons = []
    for u in units:
        area = u.get("area_m2")
        if area:
            unit_buttons.append(f"{area} м²")
    
    if not unit_buttons:
        return [["🔙 Назад"]]
    
    # Разбиваем на ряды по 3 кнопки
    rows = []
    for i in range(0, len(unit_buttons), 3):
        rows.append(unit_buttons[i:i+3])
    rows.append(["🔙 Назад"])
    
    return rows
