# CI/CD Pipeline Documentation

## Обзор

Проект использует GitHub Actions для автоматизации процесса сборки, тестирования и деплоя. Pipeline запускается при создании Pull Request в ветку `main`.

## Структура Pipeline

### 1. Test Job
- **Триггер**: При создании PR в `main` или push в `main`
- **Задачи**:
  - Сборка всех Docker образов
  - Запуск тестов для каждого сервиса
  - Проверка health endpoints
  - Валидация импортов модулей

### 2. Build Job
- **Триггер**: Только при merge PR в `main`
- **Задачи**:
  - Сборка и публикация образов в GitHub Container Registry
  - Тегирование образов (branch, PR, semver, SHA)
  - Метаданные для образов

### 3. Deploy Job
- **Триггер**: Только при merge PR в `main`
- **Задачи**:
  - Деплой в staging окружение (локально в GitHub Actions)
  - Обновление тегов образов в docker-compose.prod.yml
  - Запуск production конфигурации
  - Уведомления о завершении деплоя

**Примечание**: Текущий деплой происходит локально в GitHub Actions. Для production рекомендуется использовать отдельный сервер. Подробности в [docs/DEPLOYMENT.md](DEPLOYMENT.md).

## Переменные окружения

### GitHub Secrets

Следующие секреты должны быть настроены в репозитории:

```bash
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Database (опционально)
POSTGRES_PASSWORD=your_secure_password

# MinIO (опционально)
MINIO_SECRET_KEY=your_secure_minio_password
```

### Переменные окружения

```bash
# Docker Registry
REGISTRY=ghcr.io
IMAGE_NAME=your-username/more.tech.2025
TAG=latest

# MinIO
MINIO_ACCESS_KEY=minioadmin
MINIO_BUCKET_NAME=audio-files
```

## Настройка

### 1. Настройка GitHub Secrets

1. Перейдите в Settings → Secrets and variables → Actions
2. Добавьте следующие секреты:
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `POSTGRES_PASSWORD` (опционально)
   - `MINIO_SECRET_KEY` (опционально)

### 2. Настройка переменных окружения

1. Перейдите в Settings → Secrets and variables → Actions
2. Добавьте следующие переменные:
   - `REGISTRY=ghcr.io`
   - `IMAGE_NAME=your-username/more.tech.2025`
   - `TAG=latest`

### 3. Настройка Production

1. Скопируйте `env.prod.sample` в `.env.prod`
2. Заполните все необходимые переменные
3. Используйте `make deploy` для деплоя

## Использование

### Development

```bash
# Запуск development окружения
make up

# Проверка здоровья сервисов
make health

# Просмотр логов
make logs

# Остановка сервисов
make down
```

### Production

```bash
# Деплой в production
make deploy

# Проверка статуса
make status

# Создание бэкапа
make backup

# Восстановление из бэкапа
make restore BACKUP_FILE=backup_20250827_123456.sql
```

### CI/CD

```bash
# Локальная сборка для CI
make ci-build

# Локальное тестирование
make ci-test
```

## Структура файлов

```
.github/
├── workflows/
│   └── ci-cd.yml          # Основной pipeline

docker-compose.yml          # Development окружение
docker-compose.prod.yml     # Production окружение
docker-compose.test.yml     # Тестовое окружение
Dockerfile.test            # Dockerfile для тестов

scripts/
└── init-minio.sh          # Скрипт инициализации MinIO

tests/
├── __init__.py
└── test_health.py         # Базовые тесты

env.sample                 # Пример переменных для development
env.prod.sample            # Пример переменных для production
```

## Мониторинг

### Health Checks

Все сервисы имеют health endpoints:

- Orchestrator: `http://localhost:8000/healthz`
- STT: `http://localhost:8001/healthz`
- LLM: `http://localhost:8004/healthz`
- Avatar: `http://localhost:8005/healthz`
- Scoring: `http://localhost:8003/healthz`
- Frontend: `http://localhost:3000`

### Логи

```bash
# Логи всех сервисов
make logs

# Логи конкретного сервиса
docker compose logs -f [service]

# Логи backend сервисов
make dev-logs

# Логи frontend
make frontend-logs
```

## Troubleshooting

### Проблемы с тестами

1. Проверьте, что все секреты настроены
2. Убедитесь, что база данных доступна
3. Проверьте логи тестового контейнера

### Проблемы с деплоем

1. Проверьте переменные в `.env.prod`
2. Убедитесь, что образы собраны и опубликованы
3. Проверьте доступность production серверов

### Проблемы с MinIO

1. Проверьте инициализацию bucket'ов
2. Убедитесь в правильности credentials
3. Проверьте сетевую доступность

## Безопасность

- Все секреты хранятся в GitHub Secrets
- Образы публикуются в приватный registry
- Production переменные изолированы
- Health checks для мониторинга состояния

## Расширение

### Добавление новых тестов

1. Создайте файл в `tests/`
2. Добавьте тесты в CI pipeline
3. Обновите `Dockerfile.test` при необходимости

### Добавление новых сервисов

1. Добавьте сервис в `docker-compose.yml`
2. Обновите CI pipeline
3. Добавьте health check
4. Обновите документацию
