"""
Сервисы бота OAZIS.
"""

from .data_loader import (
    load_finance,
    load_object_finance,
    load_object_knowledge,
    get_finance_defaults,
    get_finance_units,
    get_min_lot,
    get_installment_programs,
    get_mortgage_programs,
    load_instructions,
    load_why_rizalta_text,
)

from .telegram import (
    send_message,
    send_message_inline,
    send_document,
    answer_callback_query,
)

from .calculations import (
    fmt_rub,
    normalize_unit_code,
    get_unit_by_code,
    compute_rent_cashflow,
    suggest_units_for_budget,
    generate_investment_pdf,
)

from .notifications import (
    notify_managers_telegram,
    notify_managers_email,
    send_booking_notification,
)
