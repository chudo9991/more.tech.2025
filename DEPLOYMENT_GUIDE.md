# 🚀 Руководство по деплою на VPS сервер

## 📋 **Подготовка сервера (45.144.30.194)**

### 1. **Установка Docker и зависимостей**
```bash
# Обновление системы
sudo apt update

# Установка Docker и Docker Compose
sudo apt install docker.io docker-compose git

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Создание директории проекта
sudo mkdir -p /opt/interview-ai
sudo chown $USER:$USER /opt/interview-ai
```

### 2. **Создание .env файла на сервере**
```bash
# На сервере создайте файл /opt/interview-ai/.env
cd /opt/interview-ai
nano .env
```

**Создание .env файла:**
```bash
# Скопируйте пример файла
cp env.example .env

# Отредактируйте файл, заполнив своими значениями
nano .env
```

**Структура .env файла:**
Смотрите файл `env.example` в корне проекта для полного списка переменных окружения.

### 3. **Настройка SSH ключей**
```bash
# На вашем локальном компьютере создайте SSH ключ (если нет)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# Скопируйте публичный ключ на сервер
ssh-copy-id your-username@45.144.30.194

# Или добавьте публичный ключ вручную
cat ~/.ssh/id_rsa.pub
# Скопируйте вывод и добавьте в ~/.ssh/authorized_keys на сервере
```

## 🔐 **Настройка GitHub Secrets**

В настройках репозитория GitHub добавьте следующие secrets:

### **Repository Settings → Secrets and variables → Actions**

1. **SERVER_HOST**: `45.144.30.194`
2. **SERVER_USER**: `ваш-пользователь-на-сервере`
3. **SERVER_SSH_KEY**: содержимое приватного SSH ключа (`~/.ssh/id_rsa`)

## 🌐 **Настройка домена**

### **DNS настройки**
Убедитесь, что домен `moretech2025clvb.ru` указывает на IP `45.144.30.194`:

```
A    moretech2025clvb.ru    45.144.30.194
```

### **Проверка DNS**
```bash
# Проверьте, что домен указывает на правильный IP
nslookup moretech2025clvb.ru
dig moretech2025clvb.ru
```

## 🔥 **Настройка брандмауэра**

```bash
# На сервере откройте необходимые порты
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## 🚀 **Запуск деплоя**

### **Автоматический деплой**
После настройки GitHub Secrets, деплой будет происходить автоматически при push в ветку `main`.

### **Ручной деплой (для тестирования)**
```bash
# На сервере
cd /opt/interview-ai
git clone https://github.com/your-username/more.tech.2025.git
cd more.tech.2025

# Скопируйте .env файл
cp /opt/interview-ai/.env .

# Запустите приложение
docker compose -f docker-compose.yml up -d
```

## 🔍 **Проверка работы**

### **Проверка контейнеров**
```bash
docker compose -f docker-compose.yml ps
```

### **Проверка логов**
```bash
docker compose -f docker-compose.yml logs -f
```

### **Проверка доступности**
```bash
# HTTP
curl http://moretech2025clvb.ru

# HTTPS
curl https://moretech2025clvb.ru

# API
curl https://moretech2025clvb.ru/api/v1/hr/sessions
```

## 🛠️ **Устранение неполадок**

### **Проблема: SSH подключение не работает**
```bash
# Проверьте SSH ключи
ssh -v your-username@45.144.30.194

# Проверьте права доступа
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

### **Проблема: Docker не запускается**
```bash
# Проверьте статус Docker
sudo systemctl status docker

# Перезапустите Docker
sudo systemctl restart docker
```

### **Проблема: Порты заняты**
```bash
# Проверьте занятые порты
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Остановите конфликтующие сервисы
sudo systemctl stop apache2
sudo systemctl stop nginx
```

## 📞 **Поддержка**

При возникновении проблем:
1. Проверьте логи GitHub Actions
2. Проверьте логи на сервере: `docker compose logs`
3. Проверьте статус контейнеров: `docker compose ps`
4. Проверьте доступность портов: `netstat -tlnp`

## ⚠️ **Важные замечания по безопасности**

- **НИКОГДА** не коммитьте файлы с секретными данными в Git
- Используйте GitHub Secrets для хранения чувствительной информации
- Регулярно обновляйте пароли и API ключи
- Используйте сильные пароли для всех сервисов
- Ограничьте доступ к серверу только необходимыми IP адресами