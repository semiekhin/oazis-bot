# OAZIS Bot — Полная база знаний

> 🔴 **ПРАВИЛО ДЛЯ CLAUDE:** В конце каждого чата, когда пользователь пишет "обнови текущую задачу для нового чата" или "/opt/oazis/sync.sh", ты ОБЯЗАН:
> 1. Обновить CURRENT_TASK.md — текущая задача и следующий шаг
> 2. Обновить KNOWLEDGE.md — добавить ВСЁ что сделано в этом чате
> 3. Дать команды для копирования и выполнения
>
> Следующий чат должен знать ВСЁ что знает текущий!

---

## 🔧 WORKFLOW С GITHUB

### Репозиторий
- URL: https://github.com/semiekhin/oazis-bot
- Тип: публичный (чтобы Claude мог читать)
- Ветка: main

### Синхронизация
После ЛЮБЫХ изменений:
```bash
/opt/oazis/sync.sh
```

### Работа с новым чатом
1. Пишешь: `Продолжаем OAZIS Bot: https://raw.githubusercontent.com/semiekhin/oazis-bot/main/PROJECT.md?v=X`
2. Claude читает PROJECT.md → KNOWLEDGE.md → понимает всё
3. В конце: "обнови текущую задачу" или просто `/opt/oazis/sync.sh`

### Кэш GitHub
Raw-файлы кэшируются ~5 мин. Меняй ?v=1 → ?v=2 для сброса.

---

## 🏗 АРХИТЕКТУРА

### Сервер
- IP: 72.56.64.91
- Путь: /opt/oazis
- Бот: @OazisAI_Bot
- Сервис: systemctl restart oazis-bot

### Стек
- Python 3 + FastAPI
- Telegram Bot API (webhook + Cloudflare)
- OpenAI API (Chat Completions API!)
- JSON-конфиги

### Структура
```
/opt/oazis/
├── app.py                      # Роутинг webhook, callback обработчики
├── config/settings.py          # Настройки из .env (load_dotenv!)
├── handlers/
│   ├── __init__.py             # Экспорт обработчиков (включая handle_why_*)
│   ├── menu.py                 # Главное меню
│   ├── object_handlers.py      # Город → объект → меню, подменю "О проекте"
│   ├── units.py                # ROI_TEXTS, FINANCE_TEXTS, подбор лотов
│   ├── booking.py              # Бронирование
│   └── ai_chat.py              # AI-чат обработчик
├── services/
│   ├── telegram.py             # Telegram API
│   ├── ai_chat.py              # OpenAI Chat Completions API
│   ├── data_loader.py          # Загрузка JSON
│   ├── calculations.py         # Финансовые расчёты, портфельный алгоритм
│   └── notifications.py        # Email
├── models/state.py             # Состояние диалога
├── data/objects/
│   ├── config.json             # Список объектов
│   ├── altai/rizalta/
│   │   ├── finance.json        # unit_code, price_rub, capitalization
│   │   ├── knowledge.txt
│   │   ├── text_why_belokuricha.md
│   │   └── text_why_rizalta.md
│   ├── evpatoria/moynako/
│   └── anapa/nikolay1/
├── KNOWLEDGE.md                # ← ТЫ ЗДЕСЬ
├── PROJECT.md                  # Генерируется sync.sh
├── CURRENT_TASK.md             # Текущая задача
└── sync.sh                     # Синхронизация
```

---

## 🔑 КЛЮЧЕВЫЕ ПАТТЕРНЫ

### 1. Форматы данных юнитов
**RIZALTA** использует:
- `unit_code`: "A209", "B210", "A305"
- `price_rub`: 15251250

**Мойнако/Николай I** используют:
- `code`: "2018", "5013"
- `price`: 8500000

**Универсальный геттер:**
```python
code = u.get("code") or u.get("unit_code")
price = u.get("price") or u.get("price_rub")
```

### 2. ROI_TEXTS и FINANCE_TEXTS (handlers/units.py)
Готовые красивые тексты для RIZALTA:
```python
ROI_TEXTS = {
    "A209": """💎 <b>Студия A209 (24.5 м²)</b>...""",
    "B210": """🔥 <b>Стандарт B210 (31.6 м²)</b>...""",
    "A305": """👑 <b>Люкс A305 (38.8 м²)</b>..."""
}
FINANCE_TEXTS = { ... }  # Аналогично для рассрочки/ипотеки
```

**Использование в handle_base_roi:**
```python
if object_id == "rizalta" and unit_code:
    normalized = normalize_unit_code(unit_code)
    if normalized in ROI_TEXTS:
        await send_message_inline(chat_id, ROI_TEXTS[normalized], inline_buttons)
        return
```

### 3. Портфельный алгоритм (services/calculations.py)
`generate_investment_plan()`:
- Собирает комбинации юнитов под бюджет
- Считает прогноз капитала до 2029
- Показывает альтернативы

**Вызов для RIZALTA в handle_budget_input:**
```python
if object_id == "rizalta":
    reply_text = suggest_units_for_budget(budget, "")
    ...
    return
```

### 4. AI консультант (services/ai_chat.py)
**ВАЖНО:** Использует Chat Completions API, НЕ Responses API!
```python
response = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=messages,
    max_tokens=OPENAI_MAX_TOKENS,
)
text = response.choices[0].message.content  # НЕ response.output_text!
```

### 5. Подменю "О проекте" для RIZALTA
**object_handlers.py:**
- `show_object_about()` — показывает inline-кнопки для RIZALTA
- `handle_why_region()` — загружает text_why_belokuricha.md
- `handle_why_project()` — загружает text_why_rizalta.md

**app.py callback:**
```python
elif data.startswith("why_region_"):
    await handle_why_region(chat_id, data)
elif data.startswith("why_project_"):
    await handle_why_project(chat_id, data)
```

### 6. Кнопки юнитов (object_handlers.py)
Показывают код юнита, НЕ площадь:
```python
for u in units:
    code = u.get("code") or u.get("unit_code")
    if code:
        unit_buttons.append(code)
```

### 7. OpenAI API ключ (config/settings.py)
**ВАЖНО:** Нужен load_dotenv!
```python
import os
from dotenv import load_dotenv

load_dotenv('/opt/oazis/.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
```

---

## 📊 МАТЕМАТИЧЕСКИЕ МОДЕЛИ

### Мойнако (Евпатория)
- ROI: 11.2-11.3%, окупаемость 8-9 лет
- Рассрочка: ПВ 30%, 24 мес, 0%
- Капитализация к 2027: +19-35%, далее +8%/год

### Николай I (Анапа)
- Оператор: Cosmos Hotel Group (45%)
- Налог ИП: 6%
- NOI = GI × 55% × 94%
- Индексация ADR: +5%/год
- Cap Rate: 10%
- Загрузка: 60% средняя (пик 95% июл-авг)
- ADR: 24 333 ₽ средний (пик 40к июл-авг)

### RIZALTA (Алтай)
- 3 юнита: A209 (24.5м²), B210 (31.6м²), A305 (38.8м²)
- Капитализация к 2027: +54%, к 2029: +86%
- Точка входа: ~38% от цены
- Портфельный алгоритм с прогнозом до 2029

---

## ✅ ЧТО СДЕЛАНО

### 3 декабря 2025 — RIZALTA восстановлена
- [x] **Кнопки юнитов** — показывают A209/B210/A305 (было "24.5 м²")
  - Файл: handlers/object_handlers.py
  - Изменение: `code = u.get("code") or u.get("unit_code")`
  
- [x] **ROI_TEXTS** — красивые карточки доходности для RIZALTA
  - Файл: handlers/units.py → handle_base_roi()
  - Добавлена проверка: `if object_id == "rizalta" and normalized in ROI_TEXTS`
  
- [x] **FINANCE_TEXTS** — детальные тексты рассрочки/ипотеки
  - Файл: handlers/units.py → handle_finance_overview()
  - Аналогичная проверка для FINANCE_TEXTS
  
- [x] **Подбор лота** — портфельный алгоритм с прогнозом до 2029
  - Файл: handlers/units.py → handle_budget_input()
  - Для RIZALTA вызывает suggest_units_for_budget()
  
- [x] **finance.json RIZALTA** — добавлены unit_code, price_rub
  - Файл: data/objects/altai/rizalta/finance.json
  - Было: пустые поля в units[]
  - Стало: полные данные A209, B210, A305
  
- [x] **OpenAI API** — исправлен на Chat Completions
  - Файл: services/ai_chat.py
  - Было: `client.responses.create()`, `response.output_text`
  - Стало: `client.chat.completions.create()`, `response.choices[0].message.content`
  
- [x] **load_dotenv** — API ключ теперь загружается
  - Файл: config/settings.py
  - Добавлено: `from dotenv import load_dotenv; load_dotenv('/opt/oazis/.env')`
  
- [x] **Подменю "О проекте"** — кнопки "Почему Алтай" / "Почему RIZALTA"
  - Файл: handlers/object_handlers.py → show_object_about(), handle_why_region(), handle_why_project()
  - Файл: handlers/__init__.py → экспорт handle_why_region, handle_why_project
  - Файл: app.py → callback обработчики why_region_, why_project_

- [x] **Поиск юнитов в app.py** — поддержка обоих форматов
  - Файл: app.py
  - Добавлено: поиск по коду юнита, не только по площади

### 3 декабря 2025 — GitHub + автоматизация
- [x] Git-репозиторий github.com/semiekhin/oazis-bot (публичный)
- [x] SSH-ключ ~/.ssh/github_oazis
- [x] sync.sh — автосинхронизация
- [x] PROJECT.md с raw-ссылками
- [x] CURRENT_TASK.md для передачи задач
- [x] KNOWLEDGE.md — эта база знаний
- [x] .gitignore — секреты защищены

### 30 ноября 2025 — Мойнако + рефакторинг
- [x] Добавлен Мойнако резорт (Евпатория)
- [x] Динамическая загрузка юнитов из finance.json
- [x] Подбор лота с капитализацией
- [x] finance.json для Николай I

### Объекты
- [x] RIZALTA (Алтай) — **ПОЛНОСТЬЮ РАБОТАЕТ**
- [x] Мойнако (Евпатория) — работает
- [ ] Николай I (Анапа) — нужен полный finance.json

---

## ⚠️ ИЗВЕСТНЫЕ ПРОБЛЕМЫ

### Подменю "О проекте" — требует тестирования
Кнопки добавлены, callback обработчики добавлены, но нужно проверить в боте.

---

## 📝 КОМАНДЫ
```bash
/opt/oazis/sync.sh           # Синхронизация с GitHub
systemctl restart oazis-bot  # Перезапуск бота
journalctl -u oazis-bot -f   # Логи в реальном времени
journalctl -u oazis-bot -n 50 | grep -i "error"  # Последние ошибки
```
