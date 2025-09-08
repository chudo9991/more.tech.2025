#!/bin/bash

# Скрипт для исправления таблицы alembic_version

set -e

echo "🔧 Исправление таблицы alembic_version..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "🛑 Останавливаем orchestrator..."
docker compose stop orchestrator

echo "🗑️ Удаляем контейнер orchestrator..."
docker compose rm -f orchestrator

echo "🔧 Создаем таблицу alembic_version и устанавливаем правильную версию..."
# Создаем таблицу alembic_version и устанавливаем версию 0007 (последняя миграция)
docker compose exec -T db psql -U interview_user -d interview_ai << 'EOF'
-- Создаем таблицу alembic_version
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Устанавливаем версию 0007 (последняя миграция, так как все таблицы уже созданы)
INSERT INTO alembic_version (version_num) VALUES ('0007');

-- Проверяем результат
SELECT version_num FROM alembic_version;
EOF

echo "🔨 Пересобираем orchestrator..."
docker compose build orchestrator

echo "🚀 Запускаем orchestrator..."
docker compose up -d orchestrator

echo "⏳ Ждем запуска orchestrator..."
sleep 15

echo "📊 Проверяем статус миграций..."
docker compose exec orchestrator alembic current

echo "✅ Проверяем статус всех контейнеров..."
docker compose ps

echo "🎉 Исправление завершено!"
