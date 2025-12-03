"""
Обработчик свободного текста — AI-консультант.
"""

from services.telegram import send_message_inline
from services.ai_chat import ask_ai_about_project
from services.data_loader import load_finance
from services.calculations import normalize_unit_code, fmt_rub


def format_finance_unit_answer(finance: dict, unit_code: str) -> str:
    """
    Формирует текст с расчётом доходности по юниту.
    """
    from services.calculations import get_unit_by_code, compute_rent_cashflow, get_finance_defaults
    
    u = get_unit_by_code(finance, unit_code)
    if not u:
        return (
            f"Пока нет готового инвест-расчёта по юниту {unit_code}. "
            "Лучше подключить менеджера проекта и посчитать сценарий под ваш бюджет. 💬"
        )
    
    title = u.get("title") or f"Апартамент {unit_code}"
    area = u.get("area_m2")
    price = float(u.get("price_rub", 0) or 0)
    defaults = get_finance_defaults(finance)
    
    rent = compute_rent_cashflow(u, defaults)
    
    cap = u.get("capitalization_projection", {}) or {}
    cap_list = cap.get("total_return_pct_by_year", []) or []
    
    lines = []
    lines.append(f"📊 Расчёт доходности по апартаменту {unit_code}")
    lines.append("")
    lines.append("🏡 <b>Объект</b>")
    lines.append(f"• {title}")
    if area:
        lines.append(f"• Площадь: {area} м²")
    lines.append(f"• Цена по договору: {fmt_rub(price)}")
    lines.append("")
    
    lines.append("🏨 <b>Арендный поток (упрощённый сценарий)</b>")
    lines.append(f"• Валовая выручка/год: ~{fmt_rub(rent['gross_year_rub'])}")
    lines.append(f"• Чистый доход/год: ~{fmt_rub(rent['net_year_rub'])}")
    lines.append(f"• ROI по аренде: ~{rent['roi_year_pct']:.2f}% годовых")
    lines.append("")
    
    if cap_list:
        lines.append("📈 <b>Рост стоимости и совокупная доходность</b>")
        for row in cap_list[:5]:
            year = row.get("year")
            pct = row.get("total_return_pct")
            if year and pct is not None:
                lines.append(f"• {year}: ~{pct}%")
        lines.append("")
    
    lines.append(
        "Если хотите, могу подобрать сценарий под ваш бюджет. 💬"
    )
    
    return "\n".join(lines)


async def handle_free_text(chat_id: int, text: str):
    """
    Обработка свободного текста — передача в AI.
    """
    low = text.lower()
    
    # Проверяем специальные запросы на доходность
    if "доходност" in low:
        finance = load_finance()
        if finance:
            # A209
            if "a209" in low or "а209" in low or " 209" in low:
                answer = format_finance_unit_answer(finance, "A209")
                await send_message_inline(
                    chat_id,
                    answer,
                    [[
                        {"text": "🎯 Подобрать лот", "callback_data": "select_lot"},
                        {"text": "🔥 Вызвать менеджера", "callback_data": "call_manager"}
                    ]]
                )
                return
            
            # B210
            if "b210" in low or "в210" in low:
                answer = format_finance_unit_answer(finance, "B210")
                await send_message_inline(
                    chat_id,
                    answer,
                    [[
                        {"text": "🎯 Подобрать лот", "callback_data": "select_lot"},
                        {"text": "🔥 Вызвать менеджера", "callback_data": "call_manager"}
                    ]]
                )
                return
            
            # A305
            if "a305" in low or "а305" in low or " 305" in low:
                answer = format_finance_unit_answer(finance, "A305")
                await send_message_inline(
                    chat_id,
                    answer,
                    [[
                        {"text": "🎯 Подобрать лот", "callback_data": "select_lot"},
                        {"text": "🔥 Вызвать менеджера", "callback_data": "call_manager"}
                    ]]
                )
                return
    
    # Обычный AI ответ
    answer = ask_ai_about_project(text)
    
    inline_buttons = [
        [
            {"text": "🎯 Подобрать лот", "callback_data": "select_lot"},
            {"text": "🔥 Вызвать менеджера", "callback_data": "call_manager"}
        ]
    ]
    
    await send_message_inline(chat_id, answer, inline_buttons)
