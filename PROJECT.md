# OAZIS Bot — Паспорт проекта

## Суть
Telegram-бот агрегатор курортной недвижимости. Помогает инвесторам выбрать апартаменты, рассчитать доходность, оформить бронь.

## Сервер
- IP: 72.56.64.91
- Путь: /opt/oazis
- Бот: @OazisAI_Bot
- Сервис: systemctl restart oazis-bot

## Стек
- Python 3 + FastAPI
- Telegram Bot API (webhook через Cloudflare)
- OpenAI API (AI-консультант)
- JSON-конфиги для данных объектов

## Активные объекты
- ✅ RIZALTA (Алтай) — полностью работает
- ✅ Мойнако резорт (Евпатория) — полностью работает  
- ⏳ Николай I (Анапа) — знания есть, нужен finance.json

## Что сделано
- Динамическая загрузка юнитов из finance.json
- Кнопки юнитов по площади (не хардкод)
- Подбор лота с капитализацией (+8%/год после сдачи)
- Расчёт ROI из данных объекта

## TODO
- [ ] Заполнить finance.json для Николай I (модель из 1005_расчет.pdf)
- [ ] Сделать AI-консультанта динамическим (сейчас хардкод RIZALTA)
- [ ] Добавить остальные 9 объектов
- [ ] Внедрить Spec Kit для управления разработкой

## Математическая модель Николай I
- Комиссия оператора: 45%
- Налог ИП: 6%  
- Индексация ADR: +5%/год
- Cap Rate: 10%
- Формула: NOI = GI × 55% × 94%

## Кодовая база (raw-ссылки для Claude)

### Главные файлы
- [app.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/app.py)
- [config/settings.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/config/settings.py)

### Handlers
- [handlers/menu.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/menu.py)
- [handlers/object_handlers.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/object_handlers.py)
- [handlers/units.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/units.py)
- [handlers/booking.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/booking.py)
- [handlers/ai_chat.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/handlers/ai_chat.py)

### Services
- [services/telegram.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/telegram.py)
- [services/ai_chat.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/ai_chat.py)
- [services/data_loader.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/data_loader.py)
- [services/calculations.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/calculations.py)
- [services/notifications.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/services/notifications.py)

### Models
- [models/state.py](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/models/state.py)

### Data
- [data/objects/config.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/config.json)
- [data/objects/altai/rizalta/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/altai/rizalta/finance.json)
- [data/objects/evpatoria/moynako/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/evpatoria/moynako/finance.json)
- [data/objects/anapa/nikolay1/finance.json](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/data/objects/anapa/nikolay1/finance.json)

### Документация
- [TODO.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/TODO.md)
- [CHANGELOG.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/CHANGELOG.md)
- [docs/FINANCE_MODEL.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/docs/FINANCE_MODEL.md)

## Контакты
Разработка: Claude + Сергей
