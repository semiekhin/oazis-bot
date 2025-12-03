#!/bin/bash
cd /opt/oazis

echo "🔄 Синхронизация OAZIS Bot..."

# Собираем PROJECT.md
cat > /opt/oazis/PROJECT.md << 'HEADER'
# OAZIS Bot — Паспорт проекта

> ⚠️ **ВАЖНО:** Сначала прочитай [KNOWLEDGE.md](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/KNOWLEDGE.md) — там вся база знаний проекта!

## Сервер
- IP: 72.56.64.91
- Путь: /opt/oazis
- Бот: @OazisAI_Bot
- Сервис: systemctl restart oazis-bot

HEADER

# Вставляем текущую задачу
cat /opt/oazis/CURRENT_TASK.md >> /opt/oazis/PROJECT.md
echo "" >> /opt/oazis/PROJECT.md

cat >> /opt/oazis/PROJECT.md << 'MIDDLE'
---

## Все файлы проекта (raw-ссылки)
MIDDLE

# Список файлов
find /opt/oazis \( -name "*.py" -o -name "*.json" -o -name "*.md" -o -name "*.txt" \) | grep -v venv | grep -v __pycache__ | grep -v ".git" | sort | while read f; do
    REL_PATH=${f#/opt/oazis/}
    echo "- [$REL_PATH](https://raw.githubusercontent.com/semiekhin/oazis-bot/main/$REL_PATH)" >> /opt/oazis/PROJECT.md
done

# Git
git add .
git commit -m "Sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null && git push || echo "Нет изменений"

echo "✅ Готово!"
