"""
Обработчики событий бота OAZIS.
"""

# Меню и навигация
from .menu import (
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
    handle_ai_consultation,
    handle_contact_manager,
)

# Юниты: ROI, рассрочка, планировки
from .units import (
    handle_base_roi,
    handle_unit_roi,
    handle_finance_overview,
    handle_layouts,
    handle_select_lot,
    handle_budget_input,
    handle_format_input,
    handle_download_pdf,
)

# Запись на показ
from .booking import (
    handle_online_show_start,
    handle_call_manager,
    handle_contact_shared,
    handle_quick_contact,
    handle_booking_step,
)

# AI чат
from .ai_chat import (
    handle_free_text,
)

# Обработчики объекта
from .object_handlers import (
    show_object_about,
    show_object_calculations,
    show_object_layouts,
    start_lot_selection,
    start_showing_booking,
    handle_choose_unit_for_roi,
    handle_choose_unit_for_finance,
    handle_why_region,
    handle_why_project,
)
