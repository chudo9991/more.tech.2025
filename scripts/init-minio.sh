#!/bin/bash

# Скрипт для инициализации MinIO bucket'ов
# Используется в CI/CD и при первом запуске

set -e

echo "Initializing MinIO buckets..."

# Ждем, пока MinIO станет доступен
echo "Waiting for MinIO to be ready..."
until curl -f http://minio:9000/minio/health/live; do
    echo "MinIO is not ready yet, waiting..."
    sleep 5
done

echo "MinIO is ready!"

# Настраиваем MinIO клиент
mc alias set minio http://minio:9000 ${MINIO_ACCESS_KEY:-minioadmin} ${MINIO_SECRET_KEY:-minioadmin123}

# Создаем bucket для аудио файлов
echo "Creating audio-files bucket..."
mc mb minio/audio-files --ignore-existing

# Создаем bucket для аватаров (если понадобится в будущем)
echo "Creating avatars bucket..."
mc mb minio/avatars --ignore-existing

# Устанавливаем политики доступа (опционально)
echo "Setting bucket policies..."
mc policy set download minio/audio-files
mc policy set download minio/avatars

echo "MinIO initialization completed successfully!"
echo "Available buckets:"
mc ls minio/
