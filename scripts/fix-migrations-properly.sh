#!/bin/bash

# Правильное исправление проблем с миграциями

set -e

echo "🔧 Правильное исправление миграций..."

# Проверяем, что мы в правильной директории
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: docker-compose.yml не найден. Запустите скрипт из корня проекта."
    exit 1
fi

echo "🛑 Останавливаем orchestrator..."
docker compose stop orchestrator

echo "🗑️ Удаляем контейнер orchestrator..."
docker compose rm -f orchestrator

echo "🔍 Проверяем состояние базы данных..."
# Проверяем, существует ли таблица alembic_version
ALEMBIC_EXISTS=$(docker compose exec -T db psql -U interview_user -d interview_ai -t -c "
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'alembic_version'
);" | tr -d ' \n')

echo "Таблица alembic_version существует: $ALEMBIC_EXISTS"

if [ "$ALEMBIC_EXISTS" = "f" ]; then
    echo "🔧 Создаем таблицу alembic_version..."
    docker compose exec -T db psql -U interview_user -d interview_ai << 'EOF'
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
EOF
    echo "✅ Таблица alembic_version создана"
else
    echo "📊 Проверяем текущую версию в alembic_version..."
    CURRENT_VERSION=$(docker compose exec -T db psql -U interview_user -d interview_ai -t -c "SELECT version_num FROM alembic_version;" | tr -d ' \n')
    echo "Текущая версия: '$CURRENT_VERSION'"
    
    # Если версия неправильная, исправляем
    if [ "$CURRENT_VERSION" = "0006_add_vacancy_section_keywords" ]; then
        echo "🔧 Исправляем неправильную версию..."
        docker compose exec -T db psql -U interview_user -d interview_ai << 'EOF'
UPDATE alembic_version SET version_num = '0005' WHERE version_num = '0006_add_vacancy_section_keywords';
EOF
        echo "✅ Версия исправлена на 0005"
    fi
fi

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

echo "🎉 Исправление завершено!"
