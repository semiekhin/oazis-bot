"""
OAZIS Telegram Bot
Агентство недвижимости - курортные объекты России.

Модульная архитектура:
- config/     - настройки
- models/     - состояния
- services/   - бизнес-логика
- handlers/   - обработчики событий
"""

from fastapi import FastAPI, Request
from typing import Dict, Any

from config.settings import (
    TELEGRAM_BOT_TOKEN,
    MAIN_MENU_BUTTONS,
    get_cities,
    get_city_by_id,
)
from models.state import (
    get_dialog_state,
    set_dialog_state,
    clear_dialog_state,
    clear_user_state,
    get_budget,
    save_budget,
    is_in_booking_flow,
    get_selected_city,
    get_selected_object,
    set_selected_city,
    DialogStates,
)
from services.telegram import send_message, send_message_inline, answer_callback_query
from services.calculations import normalize_unit_code

from handlers import (
    # Меню
    handle_start,
    handle_help,
    handle_back,
    handle_back_to_objects,
    handle_show_cities,
    handle_city_selected,
    handle_show_objects,
    handle_object_selected,
    handle_about_project,
    handle_calculations_menu,
    handle_choose_unit_for_roi,
    handle_choose_unit_for_finance,
    handle_ai_consultation,
    handle_contact_manager,
    
    # Юниты
    handle_base_roi,
    handle_finance_overview,
    handle_layouts,
    handle_select_lot,
    handle_budget_input,
    handle_format_input,
    handle_download_pdf,
    
    # Запись на показ
    handle_online_show_start,
    handle_contact_shared,
    handle_quick_contact,
    handle_booking_step,
    
    # AI
    handle_free_text,
    handle_why_region,
    handle_why_project,
)


app = FastAPI(title="OAZIS Bot")


@app.get("/")
async def health():
    return {"ok": True, "bot": "OAZIS"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        upd = await request.json()
    except Exception as e:
        print(f"[WEBHOOK] JSON parse error: {e}")
        return {"ok": False}
    
    print(f"[WEBHOOK] update: {upd}")
    
    # Callback Query (inline-кнопки)
    callback_query = upd.get("callback_query")
    if callback_query:
        await process_callback(callback_query)
        return {"ok": True}
    
    # Message
    msg = upd.get("message") or upd.get("edited_message")
    if not msg:
        return {"ok": True}
    
    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()
    
    # Контакт
    contact_data = msg.get("contact")
    if contact_data:
        await handle_contact_shared(chat_id, contact_data)
        return {"ok": True}
    
    if not text:
        return {"ok": True}
    
    user_info = msg.get("from", {})
    await process_message(chat_id, text, user_info)
    return {"ok": True}


async def process_callback(callback: Dict[str, Any]):
    callback_id = callback.get("id")
    data = callback.get("data", "")
    message = callback.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    from_user = callback.get("from", {})
    username = from_user.get("username", "")
    
    if not chat_id:
        return
    
    if callback_id:
        await answer_callback_query(callback_id)
    
    # Роутинг callback_data
    if data == "download_pdf":
        await handle_download_pdf(chat_id, username)
    elif data == "select_lot":
        await handle_select_lot(chat_id)
    elif data in ("call_manager", "online_show"):
        await handle_online_show_start(chat_id)
    elif data == "calculate_roi":
        await handle_base_roi(chat_id)
    elif data == "get_layouts":
        await handle_layouts(chat_id)
    elif data.startswith("roi_"):
        unit_code = data[4:]
        await handle_base_roi(chat_id, unit_code=unit_code)
    elif data.startswith("finance_"):
        unit_code = data[8:]
        await handle_finance_overview(chat_id, unit_code=unit_code)
    elif data.startswith("layout_"):
        unit_code = data[7:]
        await handle_layouts(chat_id, unit_code=unit_code)
    elif data.startswith("city_"):
        city_id = data[5:]
        await handle_city_selected(chat_id, city_id)
    elif data.startswith("object_"):
        parts = data[7:].split("_", 1)
        if len(parts) == 2:
            city_id, object_id = parts
            await handle_object_selected(chat_id, city_id, object_id)
    elif data.startswith("why_region_"):
        # Почему Алтай
        await handle_why_region(chat_id, data)
    elif data.startswith("why_project_"):
        # Почему RIZALTA
        await handle_why_project(chat_id, data)
    elif data == "back_to_object_menu":
        from handlers.object_handlers import show_object_menu
        await show_object_menu(chat_id)


async def process_message(chat_id: int, text: str, user_info: Dict[str, Any]):
    state = get_dialog_state(chat_id)
    
    # === Команды ===
    if text.startswith("/start"):
        await handle_start(chat_id, text, user_info)
        return
    
    if text == "/help":
        await handle_help(chat_id)
        return
    
    # === Кнопки главного меню ===
    if text == "🏢 Выбрать объект":
        await handle_show_cities(chat_id)
        return
    
    if text == "💬 Подобрать по запросу":
        await handle_ai_consultation(chat_id)
        return
    
    if text == "📞 Связаться с менеджером":
        await handle_contact_manager(chat_id)
        return
    
    # === Навигация ===
    if text in ("🔙 Назад", "⬅️ Назад", "Назад"):
        await handle_back(chat_id)
        return
    
    if text == "🔙 К списку объектов":
        await handle_back_to_objects(chat_id)
        return
    
    # === Выбор города ===
    if state == DialogStates.CHOOSING_CITY:
        for city in get_cities():
            if city["name"] in text or f"{city['icon']} {city['name']}" == text:
                await handle_city_selected(chat_id, city["id"])
                return
    
    # === Выбор объекта ===
    if state == DialogStates.CHOOSING_OBJECT:
        city_id = get_selected_city(chat_id)
        if city_id:
            city = get_city_by_id(city_id)
            for obj in city.get("objects", []):
                if obj["name"] in text or f"🏠 {obj['name']}" in text:
                    await handle_object_selected(chat_id, city_id, obj["id"])
                    return
    
    # === Меню объекта ===
    if state == DialogStates.IN_OBJECT_MENU or get_selected_object(chat_id):
        if "📖 О проекте" in text:
            await handle_about_project(chat_id)
            return
        if "💰 Расчёты" in text:
            await handle_calculations_menu(chat_id)
            return
        if "📊 Рентабельность/доходность" in text:
            await handle_choose_unit_for_roi(chat_id)
            return
        if "💳 Рассрочка и ипотека" in text:
            await handle_choose_unit_for_finance(chat_id)
            return
        if "🎯 Подобрать лот" in text:
            await handle_select_lot(chat_id)
            return
        if "📎 Получить планировки" in text:
            await handle_layouts(chat_id)
            return
        if "🔥 Записаться на показ" in text:
            await handle_online_show_start(chat_id)
            return
    
    # === Выбор юнита для расчётов (динамически из finance.json) ===
    from services.data_loader import load_object_finance
    city_id_for_unit = get_selected_city(chat_id)
    object_id_for_unit = get_selected_object(chat_id)
    selected_unit_code = None
    if city_id_for_unit and object_id_for_unit:
        finance_for_unit = load_object_finance(city_id_for_unit, object_id_for_unit)
        if finance_for_unit and "units" in finance_for_unit:
            # Ищем юнит по площади (кнопка "27.91 м²" -> area_m2 = 27.91)
            for u in finance_for_unit["units"]:
                area = u.get("area_m2")
                code = u.get("code") or u.get("unit_code")
                if (area and text == f"{area} м²") or (code and text == code):
                    selected_unit_code = u.get("code") or u.get("unit_code")
                    break
    
    if selected_unit_code:
        state = get_dialog_state(chat_id)
        
        if state == DialogStates.CHOOSE_ROI_UNIT:
            await handle_base_roi(chat_id, unit_code=selected_unit_code)
            return
        
        if state == DialogStates.CHOOSE_FINANCE_UNIT:
            await handle_finance_overview(chat_id, unit_code=selected_unit_code)
            return
    
    # === Диалоговые состояния ===
    if state == DialogStates.CHOOSE_UNIT_ASK_BUDGET:
        await handle_budget_input(chat_id, text)
        return
    
    if state == DialogStates.CHOOSE_UNIT_ASK_FORMAT:
        await handle_format_input(chat_id, text)
        return
    
    if state == DialogStates.ASK_CONTACT_FOR_CALLBACK:
        if text == "✍️ Ввести вручную":
            await send_message(chat_id, "Напишите ваш телефон или @username:")
            return
        await handle_quick_contact(chat_id, text)
        return
    
    if is_in_booking_flow(chat_id):
        await handle_booking_step(chat_id, text)
        return
    
    # === AI консультация ===
    if state == DialogStates.AI_CONSULTATION:
        await handle_free_text(chat_id, text)
        return
    
    # === Свободный текст → AI ===
    await handle_free_text(chat_id, text)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
