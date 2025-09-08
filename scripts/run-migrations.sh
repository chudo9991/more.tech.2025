#!/bin/bash

# Скрипт для запуска миграций базы данных на продакшене

set -e

echo "🔄 Запуск миграций базы данных..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

# Проверяем, что контейнеры запущены
if ! docker compose ps | grep -q "orchestrator.*Up"; then
    echo "❌ Ошибка: Контейнер orchestrator не запущен. Сначала запустите docker compose up -d"
    exit 1
fi

echo "📊 Проверка текущего состояния миграций..."
docker compose exec orchestrator alembic current

echo "🚀 Применение миграций..."
docker compose exec orchestrator alembic upgrade head

echo "✅ Миграции успешно применены!"

echo "📊 Проверка финального состояния..."
docker compose exec orchestrator alembic current

echo "🎉 Готово! База данных обновлена."
