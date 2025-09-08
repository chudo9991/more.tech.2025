# 🚨 Исправление проблемы с базой данных на продакшене

## ❌ **Проблема**
На продакшене возникает ошибка:
```
KeyError: '0006_add_vacancy_section_keywords'
```

## 🔍 **Причина**
Проблема с цепочкой миграций Alembic. В базе данных есть неправильная запись о версии миграции, которая ссылается на несуществующий revision ID.

## ✅ **Решение**

### **Вариант 1: Исправление цепочки миграций (рекомендуется)**

1. **Обновите код на сервере:**
```bash
# На сервере
cd /opt/interview-ai
git pull origin main
```

2. **Используйте скрипт исправления:**
```bash
chmod +x scripts/fix-migration-chain.sh
./scripts/fix-migration-chain.sh
```

3. **Или выполните вручную:**
```bash
# Останавливаем orchestrator
docker compose -f docker-compose.yml stop orchestrator

# Удаляем контейнер
docker compose -f docker-compose.yml rm -f orchestrator

# Исправляем запись в базе данных
docker compose -f docker-compose.yml exec -T db psql -U interview_user -d interview_ai << 'EOF'
UPDATE alembic_version SET version_num = '0005' WHERE version_num = '0006_add_vacancy_section_keywords';
EOF

# Пересобираем
docker compose -f docker-compose.yml build orchestrator

# Запускаем
docker compose -f docker-compose.yml up -d orchestrator

# Ждем запуска
sleep 10

# Проверяем миграции
docker compose -f docker-compose.yml exec orchestrator alembic current
```

4. **Проверьте логи orchestrator:**
```bash
docker compose -f docker-compose.yml logs orchestrator
```

Вы должны увидеть:
```
Running database migrations...
INFO  [alembic.runtime.migration] Context impl PostgreSQLImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 0001 -> 0002, Extend vacancies table with BA fields
INFO  [alembic.runtime.migration] Running upgrade 0002 -> 0003, Add vacancy_code to sessions table
...
Starting application...
```

### **Вариант 2: Ручной запуск миграций**

Если автоматический запуск не сработал:

1. **Запустите миграции вручную:**
```bash
# На сервере
cd /opt/interview-ai
docker compose -f docker-compose.yml exec orchestrator alembic upgrade head
```

2. **Проверьте результат:**
```bash
docker compose -f docker-compose.yml exec orchestrator alembic current
```

### **Вариант 3: Использование скрипта**

1. **Скопируйте скрипт на сервер:**
```bash
# На сервере
cd /opt/interview-ai
chmod +x scripts/run-migrations.sh
./scripts/run-migrations.sh
```

## 🔍 **Проверка исправления**

После применения миграций проверьте:

1. **Статус контейнеров:**
```bash
docker compose -f docker-compose.yml ps
```

2. **Логи orchestrator:**
```bash
docker compose -f docker-compose.yml logs orchestrator --tail=20
```

3. **Доступность API:**
```bash
curl https://moretech2025clvb.ru/healthz
curl https://moretech2025clvb.ru/api/v1/hr/statistics
```

4. **Создание вакансии:**
Попробуйте создать вакансию через веб-интерфейс - ошибка должна исчезнуть.

## 📊 **Список миграций**

Проверьте, что все миграции применены:
```bash
docker compose -f docker-compose.yml exec orchestrator alembic history
```

Должны быть применены:
- `0001` - Initial schema
- `0002` - Extend vacancies table (добавляет vacancy_code)
- `0003` - Add vacancy_code to sessions
- `0004` - Extend questions table
- `0005` - Add smart scenario tables
- `0006` - Add vacancy section keywords
- `0007` - Add contextual questions table

## 🚨 **Если проблема не решается**

1. **Проверьте подключение к базе данных:**
```bash
docker compose -f docker-compose.yml exec db psql -U interview_user -d interview_ai -c "\d vacancies"
```

2. **Проверьте переменные окружения:**
```bash
docker compose -f docker-compose.yml exec orchestrator env | grep DATABASE
```

3. **Проверьте логи базы данных:**
```bash
docker compose -f docker-compose.yml logs db --tail=20
```

## 📞 **Поддержка**

Если проблема не решается:
1. Сохраните логи: `docker compose logs > logs.txt`
2. Проверьте статус миграций: `docker compose exec orchestrator alembic current`
3. Обратитесь к команде разработки с подробным описанием проблемы
