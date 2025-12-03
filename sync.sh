#!/bin/bash
cd /opt/oazis

echo "🔄 Синхронизация OAZIS Bot..."

# 1. Генерируем список файлов
FILES=$(find /opt/oazis \( -name "*.py" -o -name "*.json" -o -name "*.md" -o -name "*.txt" \) | grep -v venv | grep -v __pycache__ | grep -v ".git" | sort)

# 2. Создаём новый PROJECT.md с актуальным списком
cat > /opt/oazis/PROJECT.md << 'HEADER'
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
- ✅ RIZALTA (Алтай)
- ✅ Мойнако резорт (Евпатория)
- ⏳ Николай I (Анапа) — в работе

## TODO
См. [TODO.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/TODO.md)

## Математическая модель
См. [docs/FINANCE_MODEL.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/docs/FINANCE_MODEL.md)

## Все файлы проекта (raw-ссылки для Claude)
HEADER

# Добавляем ссылки на файлы
for f in $FILES; do
    REL_PATH=${f#/opt/oazis/}
    echo "- [$REL_PATH](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/$REL_PATH)" >> /opt/oazis/PROJECT.md
done

echo "" >> /opt/oazis/PROJECT.md
echo "## Контакты" >> /opt/oazis/PROJECT.md
echo "Разработка: Claude + Сергей" >> /opt/oazis/PROJECT.md

# 3. Git
git add .
git commit -m "Sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null && git push || echo "Нет новых изменений"

echo "✅ Готово!"
