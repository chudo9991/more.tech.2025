#!/bin/bash

# Скрипт для исправления цепочки миграций без потери данных

set -e

echo "🔧 Исправление цепочки миграций..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "🛑 Останавливаем orchestrator..."
docker compose stop orchestrator

echo "🗑️ Удаляем контейнер orchestrator..."
docker compose rm -f orchestrator

echo "🔧 Исправляем проблему в базе данных..."
# Подключаемся к базе данных и исправляем запись о миграции
docker compose exec -T db psql -U interview_user -d interview_ai << 'EOF'
-- Проверяем текущее состояние
SELECT version_num FROM alembic_version;

-- Если есть неправильная запись, исправляем её
UPDATE alembic_version SET version_num = '0005' WHERE version_num = '0006_add_vacancy_section_keywords';

-- Проверяем результат
SELECT version_num FROM alembic_version;
EOF

echo "🔨 Пересобираем orchestrator..."
docker compose build orchestrator

echo "🚀 Запускаем orchestrator..."
docker compose up -d orchestrator

echo "⏳ Ждем запуска orchestrator..."
sleep 10

echo "📊 Проверяем статус миграций..."
docker compose exec orchestrator alembic current

echo "📋 Проверяем историю миграций..."
docker compose exec orchestrator alembic history

echo "✅ Проверяем статус всех контейнеров..."
docker compose ps

echo "🎉 Исправление завершено!"
