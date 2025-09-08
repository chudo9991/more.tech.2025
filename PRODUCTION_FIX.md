# 🚨 Исправление проблемы с базой данных на продакшене

## ❌ **Проблема**
На продакшене возникает ошибка:
```
(psycopg2.errors.UndefinedColumn) column vacancies.vacancy_code does not exist
```

## 🔍 **Причина**
Миграции базы данных не были применены на продакшене. Колонка `vacancy_code` добавляется в миграции `0002_extend_vacancies_table.py`, но она не была выполнена.

## ✅ **Решение**

### **Вариант 1: Автоматическое исправление (рекомендуется)**

1. **Обновите код на сервере:**
```bash
# На сервере
cd /opt/interview-ai
git pull origin main
```

2. **Пересоберите и перезапустите контейнеры:**
```bash
docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml build orchestrator
docker compose -f docker-compose.yml up -d
```

3. **Проверьте логи orchestrator:**
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
