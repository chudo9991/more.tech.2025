# 🚀 Руководство по развертыванию Interview AI

## 📋 **Варианты развертывания**

### **Вариант 1: Простое развертывание (без SSL)**
Для быстрого запуска за роутером с белым IP, но без HTTPS.

### **Вариант 2: Полное развертывание (с SSL)**
Для продакшена с доменом и SSL сертификатом.

---

## 🔧 **Вариант 1: Простое развертывание**

### **1. Подготовка сервера**
```bash
# Установите Docker и Docker Compose
sudo apt update
sudo apt install docker.io docker-compose

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

### **2. Настройка файлов**
```bash
# Скопируйте проект на сервер
git clone <your-repo>
cd more.tech.2025

# Создайте .env файл
cp env.sample .env
nano .env
```

### **3. Настройте .env файл**
```env
# База данных
DB_PASSWORD=your_secure_password

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=your_minio_password
```

### **4. Настройте внешний IP**
```bash
# Отредактируйте docker-compose.prod.yml
nano docker-compose.prod.yml

# Замените YOUR_DOMAIN на ваш внешний IP
# Например: VITE_API_URL=http://93.190.201.89:8000
```

### **5. Запустите систему**
```bash
# Используйте production конфигурацию
docker compose -f docker-compose.prod.yml up -d

# Проверьте статус
docker compose -f docker-compose.prod.yml ps
```

### **6. Настройте роутер**
- Откройте порты 3000, 8000, 8001, 8003, 8004, 8005
- Настройте port forwarding на ваш сервер
- Убедитесь, что брандмауэр разрешает эти порты

### **7. Проверьте доступность**
```bash
# Проверьте, что порты открыты
curl http://YOUR_EXTERNAL_IP:3000
curl http://YOUR_EXTERNAL_IP:8000/api/v1/hr/sessions
```

---

## 🔒 **Вариант 2: Полное развертывание с SSL**

### **1. Подготовка домена**
- Купите домен (например, interview-ai.com)
- Настройте DNS A-запись на ваш сервер
- Убедитесь, что домен указывает на ваш сервер

### **2. Настройка .env файла**
```env
# Добавьте в .env
DOMAIN_NAME=your-domain.com
CERTBOT_EMAIL=your-email@example.com
```

### **3. Настройте конфигурацию**
```bash
# Отредактируйте docker-compose.prod-ssl.yml
nano docker-compose.prod-ssl.yml

# Замените YOUR_DOMAIN на ваш домен
# Например: VITE_API_URL=https://interview-ai.com
```

### **4. Создайте SSL конфигурацию Nginx**
```bash
# Создайте nginx-ssl.conf
cp nginx/nginx.conf nginx/nginx-ssl.conf

# Отредактируйте для вашего домена
nano nginx/nginx-ssl.conf
```

### **5. Инициализируйте SSL**
```bash
# Создайте директории
mkdir -p certbot/conf certbot/www

# Запустите систему
docker compose -f docker-compose.prod-ssl.yml up -d nginx

# Получите SSL сертификат
docker compose -f docker-compose.prod-ssl.yml run --rm certbot

# Перезапустите nginx
docker compose -f docker-compose.prod-ssl.yml restart nginx
```

### **6. Запустите полную систему**
```bash
docker compose -f docker-compose.prod-ssl.yml up -d
```

---

## 🔧 **Настройка роутера**

### **Необходимые порты:**
- **80** (HTTP) - для редиректа на HTTPS
- **443** (HTTPS) - для основного трафика
- **3000** (Frontend) - если не используете nginx
- **8000** (API) - если не используете nginx

### **Port Forwarding:**
```
Внешний порт → Внутренний IP сервера:порт
80 → 192.168.1.100:80
443 → 192.168.1.100:443
```

---

## 🧪 **Тестирование**

### **1. Проверка доступности**
```bash
# Frontend
curl http://YOUR_IP:3000

# API
curl http://YOUR_IP:8000/api/v1/hr/sessions

# С SSL
curl -k https://YOUR_DOMAIN
```

### **2. Проверка микрофона**
- Откройте браузер
- Перейдите на ваш сайт
- Нажмите "Запросить доступ к микрофону"
- Разрешите доступ в браузере

### **3. Проверка всех сервисов**
```bash
# Проверьте health checks
docker compose -f docker-compose.prod.yml ps

# Проверьте логи
docker compose -f docker-compose.prod.yml logs frontend
docker compose -f docker-compose.prod.yml logs orchestrator
```

---

## 🔄 **Обновление системы**

### **Обновление кода:**
```bash
git pull
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

### **Обновление SSL (если используется):**
```bash
docker compose -f docker-compose.prod-ssl.yml run --rm certbot renew
docker compose -f docker-compose.prod-ssl.yml restart nginx
```

---

## 🚨 **Устранение неполадок**

### **Проблема: ERR_CONNECTION_REFUSED**
```bash
# Проверьте, что порты открыты
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Проверьте брандмауэр
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### **Проблема: Микрофон не работает**
- Убедитесь, что используется HTTPS или localhost
- Проверьте разрешения браузера
- Проверьте консоль браузера на ошибки

### **Проблема: SSL сертификат не работает**
```bash
# Проверьте логи certbot
docker compose -f docker-compose.prod-ssl.yml logs certbot

# Проверьте логи nginx
docker compose -f docker-compose.prod-ssl.yml logs nginx
```

---

## 📞 **Поддержка**

При возникновении проблем:
1. Проверьте логи: `docker compose logs <service>`
2. Проверьте статус контейнеров: `docker compose ps`
3. Проверьте сетевые порты: `netstat -tlnp`
4. Проверьте брандмауэр: `sudo ufw status`
