#!/bin/bash

# Скрипт для инициализации миграций с нуля

set -e

echo "🔄 Инициализация миграций с нуля..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "🛑 Останавливаем orchestrator..."
docker compose stop orchestrator

echo "🗑️ Удаляем контейнер orchestrator..."
docker compose rm -f orchestrator

echo "🔧 Инициализируем миграции в базе данных..."
# Подключаемся к базе данных и создаем таблицу alembic_version
docker compose exec -T db psql -U interview_user -d interview_ai << 'EOF'
-- Создаем таблицу alembic_version если её нет
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Устанавливаем начальную версию
INSERT INTO alembic_version (version_num) VALUES ('0001') ON CONFLICT (version_num) DO NOTHING;

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

echo "📋 Проверяем историю миграций..."
docker compose exec orchestrator alembic history

echo "✅ Проверяем статус всех контейнеров..."
docker compose ps

echo "🎉 Инициализация завершена!"
