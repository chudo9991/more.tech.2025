#!/bin/bash

# Скрипт для диагностики проблем с миграциями

set -e

echo "🔍 Диагностика проблем с миграциями..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "📊 Проверяем состояние базы данных..."
docker compose exec -T db psql -U interview_user -d interview_ai << 'EOF'
-- Проверяем существование таблицы alembic_version
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'alembic_version'
) as alembic_version_exists;

-- Если таблица существует, показываем её содержимое
\c interview_ai;
\dt alembic_version;

-- Показываем все таблицы в базе
\dt;
EOF

echo "📋 Проверяем файлы миграций..."
ls -la orchestrator/alembic/versions/

echo "🔧 Проверяем конфигурацию Alembic..."
docker compose exec orchestrator cat alembic.ini | grep -E "(script_location|sqlalchemy.url)"

echo "📊 Проверяем статус контейнеров..."
docker compose ps

echo "🎯 Диагностика завершена!"
