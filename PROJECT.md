# OAZIS Bot — Паспорт проекта

## Суть
Telegram-бот агрегатор курортной недвижимости. Помогает инвесторам выбрать апартаменты, рассчитать доходность, оформить бронь.

## Сервер
- IP: 72.56.64.91
- Путь: /opt/oazis
- Бот: @OazisAI_Bot
- Сервис: systemctl restart oazis-bot

## 🎯 ТЕКУЩАЯ ЗАДАЧА
**Протестировать RIZALTA и закоммитить изменения**

Статус (03.12.2025): **RIZALTA полностью восстановлена!**

Следующие шаги:
1. Протестировать весь флоу RIZALTA в боте
2. Проверить подменю "О проекте"
3. Заполнить finance.json для Николай I (Анапа)

---

## Стек
- Python 3 + FastAPI
- Telegram Bot API (webhook через Cloudflare)  
- OpenAI API (Chat Completions)
- JSON-конфиги для данных объектов

## Активные объекты
- ✅ RIZALTA (Алтай) — **восстановлена 03.12.2025**
- ✅ Мойнако резорт (Евпатория)
- ⏳ Николай I (Анапа) — нужен finance.json

## Документация
- [KNOWLEDGE.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/KNOWLEDGE.md) — полная база знаний
- [CURRENT_TASK.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/CURRENT_TASK.md) — текущая задача
- [TODO.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/TODO.md)

## Ключевые файлы
- [app.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/app.py)
- [handlers/units.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/units.py) — ROI_TEXTS, FINANCE_TEXTS
- [handlers/object_handlers.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/object_handlers.py)
- [services/ai_chat.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/ai_chat.py)
- [services/calculations.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/calculations.py)
- [config/settings.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/config/settings.py)
- [data/objects/altai/rizalta/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/altai/rizalta/finance.json)

## Контакты
Разработка: Claude + Сергей
