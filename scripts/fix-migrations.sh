#!/bin/bash

# Скрипт для исправления проблем с миграциями на продакшене

set -e

echo "🔧 Исправление проблем с миграциями..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "🛑 Останавливаем orchestrator..."
docker compose stop orchestrator

echo "🗑️ Удаляем контейнер orchestrator..."
docker compose rm -f orchestrator

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
