# Настройка VPS для деплоя

## Шаг 1: Аренда VPS сервера

### Рекомендуемые провайдеры:
- **DigitalOcean** - $5/месяц (1GB RAM, 1 CPU)
- **Hetzner** - €3/месяц (2GB RAM, 1 CPU)
- **AWS EC2** - t3.micro (бесплатно 12 месяцев)
- **Vultr** - $2.50/месяц (512MB RAM, 1 CPU)

### Минимальные требования:
- **RAM**: 2GB (рекомендуется 4GB)
- **CPU**: 1 ядро
- **Диск**: 20GB
- **ОС**: Ubuntu 20.04 или 22.04

## Шаг 2: Подготовка сервера

### 2.1. Подключение к серверу
```bash
ssh root@YOUR_SERVER_IP
```

### 2.2. Обновление системы
```bash
apt update && apt upgrade -y
```

### 2.3. Установка Docker
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Добавление пользователя в группу docker
usermod -aG docker $USER

# Включение автозапуска Docker
systemctl enable docker
systemctl start docker
```

### 2.4. Установка Docker Compose
```bash
# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker-compose --version
```

### 2.5. Создание пользователя для приложения
```bash
# Создание пользователя
adduser interview-ai
usermod -aG docker interview-ai

# Переключение на пользователя
su - interview-ai
```

### 2.6. Создание директории для приложения
```bash
mkdir -p /opt/interview-ai
cd /opt/interview-ai
```

## Шаг 3: Настройка SSH ключей

### 3.1. Генерация SSH ключа на вашем компьютере
```bash
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

### 3.2. Копирование публичного ключа на сервер
```bash
ssh-copy-id interview-ai@YOUR_SERVER_IP
```

### 3.3. Проверка подключения
```bash
ssh interview-ai@YOUR_SERVER_IP
```

## Шаг 4: Настройка GitHub Secrets

В вашем GitHub репозитории перейдите в **Settings → Secrets and variables → Actions** и добавьте:

### 4.1. Обязательные секреты
```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### 4.2. Секреты для VPS
```
SERVER_HOST=YOUR_SERVER_IP
SERVER_USER=interview-ai
SERVER_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
your_private_ssh_key_content_here
-----END OPENSSH PRIVATE KEY-----
```

### 4.3. Опциональные секреты
```
POSTGRES_PASSWORD=your_secure_password
MINIO_SECRET_KEY=your_secure_minio_password
```

## Шаг 5: Настройка файрвола

### 5.1. Установка UFW
```bash
apt install ufw
```

### 5.2. Настройка правил
```bash
# Разрешаем SSH
ufw allow ssh

# Разрешаем порты приложения
ufw allow 3000  # Frontend
ufw allow 8000  # Orchestrator
ufw allow 8001  # STT
ufw allow 8003  # Scoring
ufw allow 8004  # LLM
ufw allow 8005  # Avatar
ufw allow 9000  # MinIO
ufw allow 9001  # MinIO Console
ufw allow 5432  # PostgreSQL (если нужно)

# Включаем файрвол
ufw enable
```

## Шаг 6: Настройка домена (опционально)

### 6.1. Покупка домена
Купите домен (например, на Namecheap, GoDaddy, или используйте бесплатный Freenom).

### 6.2. Настройка DNS
Добавьте A-запись:
```
Type: A
Name: @
Value: YOUR_SERVER_IP
TTL: 300
```

### 6.3. Настройка Nginx (для HTTPS)
```bash
# Установка Nginx
apt install nginx certbot python3-certbot-nginx

# Создание конфигурации
cat > /etc/nginx/sites-available/interview-ai << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Активация сайта
ln -s /etc/nginx/sites-available/interview-ai /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# Получение SSL сертификата
certbot --nginx -d your-domain.com
```

## Шаг 7: Первый деплой

### 7.1. Создание файла переменных окружения
```bash
cd /opt/interview-ai
cp env.prod.sample .env.prod
nano .env.prod
```

### 7.2. Заполнение переменных
```bash
# Docker Registry and Image Configuration
REGISTRY=ghcr.io
IMAGE_NAME=your-username/more.tech.2025
TAG=latest

# Database Configuration
POSTGRES_PASSWORD=your_secure_password_here

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# MinIO Configuration
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=your_secure_minio_password_here
MINIO_BUCKET_NAME=audio-files
```

### 7.3. Запуск первого деплоя
```bash
# Клонирование репозитория
git clone https://github.com/your-username/more.tech.2025.git .

# Запуск приложения
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## Шаг 8: Проверка работы

### 8.1. Проверка статуса сервисов
```bash
docker compose -f docker-compose.prod.yml ps
```

### 8.2. Проверка логов
```bash
docker compose -f docker-compose.prod.yml logs -f
```

### 8.3. Проверка доступности
```bash
# Frontend
curl http://localhost:3000

# API
curl http://localhost:8000/healthz

# MinIO
curl http://localhost:9000/minio/health/live
```

## Шаг 9: Автоматический деплой

### 9.1. Переименование workflow файла
```bash
# В вашем репозитории переименуйте файл
mv .github/workflows/ci-cd.yml .github/workflows/ci-cd.yml.backup
mv .github/workflows/ci-cd-vps.yml .github/workflows/ci-cd.yml
```

### 9.2. Создание Pull Request
Теперь при создании и merge Pull Request в ветку `main` автоматически произойдет деплой на ваш VPS.

## Мониторинг и обслуживание

### Проверка статуса
```bash
# Статус сервисов
docker compose -f docker-compose.prod.yml ps

# Использование ресурсов
docker stats

# Логи
docker compose -f docker-compose.prod.yml logs -f [service_name]
```

### Обновление приложения
```bash
# Обновление образов
docker compose -f docker-compose.prod.yml pull

# Перезапуск сервисов
docker compose -f docker-compose.prod.yml up -d
```

### Бэкап базы данных
```bash
# Создание бэкапа
docker compose -f docker-compose.prod.yml exec db pg_dump -U postgres interview_ai > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление
docker compose -f docker-compose.prod.yml exec -T db psql -U postgres interview_ai < backup_file.sql
```

## Troubleshooting

### Проблемы с подключением
```bash
# Проверка SSH
ssh -v interview-ai@YOUR_SERVER_IP

# Проверка файрвола
ufw status
```

### Проблемы с Docker
```bash
# Перезапуск Docker
systemctl restart docker

# Очистка неиспользуемых ресурсов
docker system prune -a
```

### Проблемы с приложением
```bash
# Проверка логов
docker compose -f docker-compose.prod.yml logs [service_name]

# Перезапуск сервиса
docker compose -f docker-compose.prod.yml restart [service_name]
```

## Стоимость

### Примерные расходы в месяц:
- **VPS**: $5-10
- **Домен**: $1-10 (если нужен)
- **Итого**: $6-20/месяц

### Оптимизация затрат:
- Используйте бесплатные тарифы (AWS Free Tier)
- Выбирайте дешевые регионы
- Используйте spot instances (если возможно)
