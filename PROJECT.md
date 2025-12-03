# OAZIS Bot — Паспорт проекта

> ⚠️ **ВАЖНО:** Сначала прочитай [KNOWLEDGE.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/KNOWLEDGE.md) — там вся база знаний проекта!

## Сервер
- IP: 72.56.64.91
- Путь: /opt/oazis
- Бот: @OazisAI_Bot
- Сервис: systemctl restart oazis-bot

## 🎯 ТЕКУЩАЯ ЗАДАЧА
**Сделать AI-консультант умным: поиск по всей базе объектов**

Последнее действие: Заполнен finance.json для Николай I с реальными данными из расчётов Cosmos

Следующий шаг:
1. Переписать services/ai_chat.py — загружать ВСЕ объекты
2. AI должен понимать критерии (бюджет, семья, климат) и искать по всей базе
3. Если пользователь в контексте объекта — уточнять "Вы спрашиваете про X?"
4. Давать конкретные цифры из finance.json

---

## Все файлы проекта (raw-ссылки)
- [CHANGELOG.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/CHANGELOG.md)
- [CURRENT_TASK.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/CURRENT_TASK.md)
- [KNOWLEDGE.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/KNOWLEDGE.md)
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
