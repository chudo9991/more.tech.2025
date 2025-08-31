#!/bin/bash

# Обновление Let's Encrypt сертификатов
# Этот скрипт можно запускать через cron для автоматического обновления

COMPOSE="/usr/bin/docker compose --no-ansi"
DOCKER="/usr/bin/docker"

cd /media/aleks/1TB14/Projects/more.tech.2025/
$COMPOSE run certbot renew
$COMPOSE kill -s SIGHUP nginx
