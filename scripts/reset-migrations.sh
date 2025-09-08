#!/bin/bash

# Скрипт для полного сброса и пересоздания миграций

set -e

echo "🔄 Полный сброс миграций..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "🛑 Останавливаем все контейнеры..."
docker compose down

echo "🗑️ Удаляем все контейнеры..."
docker compose rm -f

echo "🗑️ Удаляем volumes (ВНИМАНИЕ: это удалит все данные!)..."
read -p "Вы уверены, что хотите удалить все данные? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker volume rm moretech2025_postgres_data || true
    docker volume rm moretech2025_minio_data || true
    docker volume rm moretech2025_caddy_data || true
    echo "✅ Volumes удалены"
else
    echo "⚠️ Volumes сохранены"
fi

echo "🔨 Пересобираем все контейнеры..."
docker compose build

echo "🚀 Запускаем все сервисы..."
docker compose up -d

echo "⏳ Ждем запуска базы данных..."
sleep 15

echo "📊 Проверяем статус миграций..."
docker compose exec orchestrator alembic current

echo "📋 Проверяем историю миграций..."
docker compose exec orchestrator alembic history

echo "✅ Проверяем статус всех контейнеров..."
docker compose ps

echo "🎉 Сброс завершен!"
