"""
AI-консультант на базе OpenAI.
"""

from typing import Dict, Any, List, Optional

from openai import OpenAI

from config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS
from services.data_loader import load_finance, load_instructions


# Инициализация клиента
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def build_finance_system_context(finance: Dict[str, Any]) -> str:
    """
    Строит контекст с финансовыми данными для AI.
    """
    completion = finance.get("completion_year", 2027)
    project = finance.get("project", "RIZALTA Resort Belokurikha")
    min_lot = finance.get("min_lot", {})
    defaults = finance.get("defaults", {})
    installments = finance.get("installment_programs", [])
    mortgages = finance.get("mortgage_programs", [])
    scenarios = finance.get("investment_scenarios", [])
    
    lines: List[str] = []
    lines.append(f"Срок сдачи объекта: {completion} год")
    lines.append("")
    lines.append("=== Финансовые параметры проекта (жёсткий контекст, цифры не придумывать) ===")
    lines.append(f"Проект: {project}")
    
    # Минимальный лот
    if min_lot:
        lines.append(
            f"Минимальный инвестиционный лот: код {min_lot.get('unit_code', 'A209')}, "
            f"цена по договору {min_lot.get('price_rub')} ₽, "
            f"реальная стоимость с учётом включённых услуг {min_lot.get('real_price_rub')} ₽ "
            f"(выгода около 150 000 ₽ за счёт включённых сервисных платежей)."
        )
        entry = min_lot.get("entry_point_rub")
        if entry:
            lines.append(f"Точка входа для минимального лота: {entry} ₽ (первоначальный платёж / пакет).")
    
    # Базовые допущения
    daily = defaults.get("daily_rate_rub")
    occ = defaults.get("occupancy_pct")
    exp = defaults.get("expenses_pct")
    if daily is not None and occ is not None and exp is not None:
        lines.append(
            "Базовые допущения по аренде для всех расчётов: "
            f"ставка аренды {daily} ₽/сутки, "
            f"средняя загрузка {occ}%, "
            f"операционные расходы {exp}% от выручки."
        )
    
    # Инвест-сценарий
    if scenarios:
        s = scenarios[0]
        roi = s.get("first_year_roi_pct")
        payback = s.get("payback_years")
        parts = ["Базовый инвест-сценарий по минимальному лоту A209:"]
        s_entry = s.get("entry_point_rub") or min_lot.get("entry_point_rub")
        if s_entry:
            parts.append(f"точка входа около {s_entry} ₽;")
        if roi:
            parts.append(f"ожидаемая доходность первого года около {roi}% годовых;")
        if payback:
            parts.append(f"ориентировочная полная окупаемость вложений около {payback} лет.")
        lines.append(" ".join(parts))
    
    # Рассрочка
    if installments:
        inst = installments[0]
        lines.append(
            "Рассрочка от застройщика: "
            f"первоначальный взнос {inst.get('first_payment_pct')}% от цены объекта, "
            f"срок {inst.get('months')} месяцев, "
            f"ставка {inst.get('rate_pct')}% годовых (как правило, = 0%, без переплаты)."
        )
    
    # Ипотека
    if mortgages:
        m = mortgages[0]
        lines.append(
            "Базовая ипотечная программа: "
            f"цена объекта {m.get('object_price_rub')} ₽, "
            f"первоначальный взнос {m.get('first_payment_rub')} ₽ ({m.get('first_payment_pct')}%), "
            f"сумма кредита {m.get('credit_amount_rub')} ₽, "
            f"срок {m.get('term_months')} месяцев, "
            f"льготный период {m.get('grace_period_months')} месяцев, "
            f"льготный платёж {m.get('reduced_payment_rub')} ₽/мес., "
            f"основной платёж {m.get('normal_payment_rub')} ₽/мес."
        )
    
    lines.append(
        "Если пользователь спрашивает про доходность, рассрочку или ипотеку — "
        "используй эти зафиксированные цифры как базу. Не придумывай новые диапазоны."
    )
    lines.append(
        "Не используй LaTeX и формулы вида [ 10 000 × 365 ]. "
        "Только обычный текст, списки и краткие расчёты словами."
    )
    
    return "\n".join(lines)


def ask_ai_about_project(user_text: str) -> str:
    """
    ИИ-консультант по проекту.
    """
    if not client:
        return (
            "ИИ-сервис временно недоступен (не настроен API-ключ). "
            "Предлагаю подключить менеджера для консультации."
        )
    
    # Загружаем инструкции и финансы
    instructions = load_instructions()
    finance = load_finance()
    if finance:
        instructions = instructions + "\n\n" + build_finance_system_context(finance)
    
    kwargs: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "instructions": instructions,
        "input": user_text,
        "max_output_tokens": OPENAI_MAX_TOKENS,
    }
    
    try:
        response = client.responses.create(**kwargs)
    except Exception as e:
        print(f"[AI] error calling Responses API: {e}")
        return (
            "Сейчас ИИ-сервис временно недоступен, но это не мешает вам получить "
            "полноценную консультацию по RIZALTA. 💬\n\n"
            "Предлагаю подключить менеджера застройщика: он подробно ответит на ваши вопросы."
        )
    
    # Извлекаем текст ответа
    text = None
    try:
        text = response.output_text
    except Exception:
        try:
            parts: List[str] = []
            output = getattr(response, "output", None)
            if output:
                for item in output:
                    content = getattr(item, "content", None)
                    if content:
                        for c in content:
                            t = getattr(c, "text", None)
                            if t:
                                parts.append(t)
            if parts:
                text = "\n".join(parts)
        except Exception as e:
            print(f"[AI] fallback parse error: {e}")
    
    if not text:
        return (
            "По этому запросу не удалось собрать развёрнутый ответ. "
            "Чтобы дать вам точные цифры, лучше подключить менеджера проекта."
        )
    
    return text
