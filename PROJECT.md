# OAZIS Bot — Паспорт проекта

## Суть
Telegram-бот агрегатор курортной недвижимости. Помогает инвесторам выбрать апартаменты, рассчитать доходность, оформить бронь.

## Сервер
- IP: 72.56.64.91
- Путь: /opt/oazis
- Бот: @OazisAI_Bot
- Сервис: systemctl restart oazis-bot

## 🎯 ТЕКУЩАЯ ЗАДАЧА
**Заполнить finance.json для Николай I (Анапа)**

Последнее действие: настроили GitHub репозиторий, sync.sh, автоматическое обновление PROJECT.md

Что уже есть:
- 7 лотов с ценами (2018, 5013, 3017, 2095, 5018, 2002, 6020)
- Модель расчёта из 1005_расчет.pdf: 45% оператор, 6% налог, сезонность
- knowledge.txt создан
- finance.json базовый — нужно заполнить

Данные из PDF расчёта (1-комн 41.4 м²):
- Загрузка по месяцам: янв 50%, фев 30%, мар 40%, апр 50%, май 70%, июн 90%, июл 95%, авг 95%, сен 90%, окт 45%, ноя 30%, дек 40%
- ADR по месяцам: низкий сезон 16-17к, высокий 28-40к
- Средняя загрузка: 60%, средний ADR: 24 333 ₽
- GI год 1: 6 211 200 ₽
- NOI год 1: 3 211 190 ₽ (ROI 15.5%)

Следующий шаг: заполнить finance.json для всех 7 лотов, нужны PDF расчётов для 2-комн и 3-комн

---

## Стек
- Python 3 + FastAPI
- Telegram Bot API (webhook через Cloudflare)  
- OpenAI API (AI-консультант)
- JSON-конфиги для данных объектов

## Активные объекты
- ✅ RIZALTA (Алтай)
- ✅ Мойнако резорт (Евпатория)
- ⏳ Николай I (Анапа) — в работе

## TODO
См. [TODO.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/TODO.md)

## Математическая модель
См. [docs/FINANCE_MODEL.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/docs/FINANCE_MODEL.md)

## Все файлы проекта (raw-ссылки для Claude)
- [CHANGELOG.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/CHANGELOG.md)
- [CURRENT_TASK.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/CURRENT_TASK.md)
- [PROJECT.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/PROJECT.md)
- [README.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/README.md)
- [TODO.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/TODO.md)
- [app.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/app.py)
- [config/__init__.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/config/__init__.py)
- [config/instructions.txt](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/config/instructions.txt)
- [config/settings.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/config/settings.py)
- [data/objects/altai/rizalta/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/altai/rizalta/finance.json)
- [data/objects/altai/rizalta/knowledge.txt](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/altai/rizalta/knowledge.txt)
- [data/objects/altai/rizalta/text_why_belokuricha.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/altai/rizalta/text_why_belokuricha.md)
- [data/objects/altai/rizalta/text_why_rizalta.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/altai/rizalta/text_why_rizalta.md)
- [data/objects/anapa/nikolay1/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/anapa/nikolay1/finance.json)
- [data/objects/anapa/nikolay1/knowledge.txt](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/anapa/nikolay1/knowledge.txt)
- [data/objects/config.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/config.json)
- [data/objects/evpatoria/moynako/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/evpatoria/moynako/finance.json)
- [data/objects/evpatoria/moynako/knowledge.txt](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/evpatoria/moynako/knowledge.txt)
- [docs/FINANCE_MODEL.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/docs/FINANCE_MODEL.md)
- [handlers/__init__.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/__init__.py)
- [handlers/ai_chat.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/ai_chat.py)
- [handlers/booking.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/booking.py)
- [handlers/menu.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/menu.py)
- [handlers/object_handlers.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/object_handlers.py)
- [handlers/units.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/units.py)
- [models/__init__.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/models/__init__.py)
- [models/state.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/models/state.py)
- [services/__init__.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/__init__.py)
- [services/ai_chat.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/ai_chat.py)
- [services/calculations.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/calculations.py)
- [services/data_loader.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/data_loader.py)
- [services/notifications.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/notifications.py)
- [services/telegram.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/telegram.py)

## Контакты
Разработка: Claude + Сергей
