# Interview AI - Система ИИ-интервью с голосовым общением

**Что строим:** AI-ассистент для первичного интервью с голосовым общением через веб-интерфейс.
**Как работает:** кандидат заходит на сайт → общается голосом с AI-аватаром → STT транскрибирует ответы → Azure GPT-4o оценивает по критериям → анализ тона голоса → всё сохраняется в БД → HR-панель показывает результаты.
**Архитектура:** Микросервисная архитектура с Docker Compose.

---

# 1) Цели и границы MVP

* Провести **полноценное интервью** по 1 вакансии (6–8 вопросов).
* Поддержать **веб-интерфейс** для кандидатов с голосовым общением.
* Получить **структурированный результат**: per-criterion баллы, общий скор, анализ тона голоса, ключевые цитаты, ссылка на аудио.
* **Админка HR:** список сессий, карточка кандидата, детальный анализ ответов, воспроизведение аудио.
* **Сроки:** хакатонная версия — без сложной саморегистрации и многоязычия.

**Вне MVP:** интеграции с ATS/CRM, календари, массовые рассылки, авто-перезвоны, сложные роли/доступы.

---

# 2) Архитектура и модули

1. **Веб-интерфейс для кандидатов (Vue.js + Element Plus)**

   * Современный UI с голосовым вводом и Voice Activity Detection (VAD).
   * Интеграция с браузерными API для записи аудио.
   * Real-time общение с AI-аватаром.
   * Автоматическая остановка записи по тишине.

2. **Orchestrator (FastAPI)**

   * Ведёт сценарий интервью, хранит состояние, маршрутизирует запросы.
   * Управляет сессиями и сообщениями.
   * Интеграция с MinIO для хранения аудио файлов.

3. **STT (Speech-to-Text)** — Whisper + VAD

   * Whisper модель для транскрипции аудио.
   * Voice Activity Detection (webrtcvad) для определения речи.
   * Поддержка русского языка.
   * Сохранение аудио в MinIO.

4. **LLM (Azure GPT-4o)**

   * Оценка ответов кандидатов по критериям.
   * Анализ тона голоса и эмоционального состояния.
   * Генерация ответов аватара.

5. **Avatar Generation**

   * Заглушка для RTSP потока AI-аватара.
   * Подготовлена для интеграции с внешними сервисами генерации аватаров.

6. **Tone & Анализ голоса**

   * Анализ тона: positive/neutral/concerned/excited/confused/confident.
   * Параметры: темп речи, паузы, длительность ответа.
   * *Важно:* эти признаки **информативны**, но не влияют на итог без явной настройки.

7. **Хранилище**

   * **PostgreSQL** для сущностей и оценок.
   * **MinIO** для аудио файлов (S3-совместимое хранилище).

8. **HR-frontend (Vue.js + Element Plus)**

   * Список сессий с фильтрами.
   * Детальная карточка кандидата с транскриптами.
   * Воспроизведение аудио записей.
   * Анализ тона голоса и оценок.

9. **Наблюдаемость**

   * Структурированные логи во всех сервисах.
   * Health checks для всех компонентов.
   * Docker Compose для оркестрации.

---

# 3) Контракты API

## 3.1. Создание сессии

```json
{
  "candidate_name": "Иван Иванов",
  "vacancy_id": "SWE_BACK_001",
  "contact_info": "ivan@example.com"
}
```

## 3.2. Сохранение сообщения

```json
{
  "session_id": "uuid",
  "message_id": "msg-uuid",
  "text": "Транскрипт ответа",
  "message_type": "user",
  "timestamp": "2025-08-27T21:30:00Z",
  "audio_url": "minio://audio-files/session_uuid_filename.webm",
  "transcription_confidence": 0.95,
  "tone_analysis": "positive"
}
```

## 3.3. Анализ тона голоса

```json
{
  "tone": "positive",
  "confidence": 0.84,
  "emotion": "excited"
}
```

---

# 4) Data Flow

1. **Создание сессии** → кандидат получает уникальную ссылку.
2. **Начало интервью** → аватар приветствует кандидата.
3. **Голосовое общение** → кандидат отвечает на вопросы голосом.
4. **STT обработка** → аудио транскрибируется в текст.
5. **LLM анализ** → оценка ответа и анализ тона.
6. **Сохранение** → все данные сохраняются в БД и MinIO.
7. **HR анализ** → результаты доступны в HR панели.

---

# 5) User Journey

**Кандидат:** 
- Переходит по ссылке на интервью
- Видит приветствие от AI-аватара
- Отвечает на вопросы голосом
- Получает завершение интервью

**HR/аналитик:** 
- Открывает HR панель
- Видит список сессий и итоговые баллы
- Заходит в карточку кандидата
- Читает транскрипты, слушает аудио
- Анализирует тон голоса и оценки
- Принимает решение

---

# 6) Технические особенности

* **Voice Activity Detection (VAD)** - автоматическая остановка записи по тишине
* **Web Audio API** - запись аудио в браузере
* **MinIO** - S3-совместимое хранилище для аудио
* **Whisper** - высококачественная транскрипция
* **Azure GPT-4o** - современная LLM для анализа
* **Docker Compose** - простое развертывание

---

# 7) Модель данных

* `candidates(id, name, contact_info, created_at)`
* `vacancies(id, title, description, created_at)`
* `sessions(id, candidate_id, vacancy_id, status, started_at, finished_at, total_score)`
* `messages(id, session_id, message_id, text, message_type, audio_url, transcription_confidence, tone_analysis, timestamp, created_at)`

---

# 8) Эндпоинты API

## Orchestrator
* `POST /api/v1/sessions/` - создание сессии
* `POST /api/v1/sessions/messages` - сохранение сообщения
* `GET /api/v1/sessions/messages` - получение сообщений сессии
* `GET /api/v1/sessions/audio/{session_id}/{filename}` - получение аудио файла
* `GET /api/v1/hr/sessions` - список сессий для HR
* `GET /api/v1/hr/sessions/{id}/results` - результаты сессии

## STT
* `POST /api/v1/stt/transcribe-file` - транскрипция аудио файла

## LLM
* `POST /api/v1/llm/chat` - чат с LLM
* `POST /api/v1/llm/score` - оценка ответа
* `POST /api/v1/llm/analyze-tone` - анализ тона голоса

---

# 9) Как запустить проект

## Предварительные требования

* Docker и Docker Compose
* Git

## Быстрый старт

### Development

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd more.tech.2025
   ```

2. **Скопируйте файл с переменными окружения:**
   ```bash
   cp env.sample .env
   # Отредактируйте .env файл, добавив ваши API ключи
   ```

3. **Запустите все сервисы:**
   ```bash
   make up
   ```

4. **Проверьте статус:**
   ```bash
   make health
   ```

5. **Откройте приложение:**
   - Frontend: http://localhost:3000
   - HR Panel: http://localhost:3000/hr
   - Candidate Interview: http://localhost:3000/interview
   - API документация: http://localhost:8000/docs
   - MinIO консоль: http://localhost:9001

### Production

1. **Настройте production переменные:**
   ```bash
   cp env.prod.sample .env.prod
   # Отредактируйте .env.prod файл
   ```

2. **Деплой:**
   ```bash
   make deploy
   ```

## CI/CD

Проект использует GitHub Actions для автоматизации. Подробная документация: [docs/CI_CD.md](docs/CI_CD.md)

### Настройка CI/CD

1. **Настройте GitHub Secrets:**
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `POSTGRES_PASSWORD` (опционально)
   - `MINIO_SECRET_KEY` (опционально)

2. **Pipeline автоматически запускается при:**
   - Создании Pull Request в `main`
   - Merge Pull Request в `main`

## Полезные команды

```bash
# Управление сервисами
make up              # Запустить development окружение
make up-prod         # Запустить production окружение
make down            # Остановить все сервисы
make build           # Пересобрать образы
make logs            # Показать логи всех сервисов
make health          # Проверить здоровье сервисов
make status          # Показать статус сервисов

# База данных
make db-shell        # Подключиться к БД
make db-reset        # Сбросить базу данных
make backup          # Создать бэкап
make restore BACKUP_FILE=file.sql  # Восстановить из бэкапа

# MinIO
make minio-shell     # Подключиться к MinIO
make minio-init      # Инициализировать bucket'ы

# Разработка
make dev-logs        # Логи backend сервисов
make frontend-logs   # Логи frontend
make clean           # Очистить контейнеры и образы

# CI/CD
make ci-build        # Сборка для CI
make ci-test         # Тестирование для CI
make deploy          # Деплой в production
```

## Структура проекта

```
more.tech.2025/
├── docker-compose.yml      # Конфигурация всех сервисов
├── env.sample              # Пример переменных окружения
├── orchestrator/           # Основной сервис (FastAPI)
├── stt/                    # Speech-to-Text сервис
├── llm/                    # LLM сервис (Azure GPT-4o)
├── avatar/                 # Avatar сервис
├── scoring/                # Legacy LLM-оценка сервис
├── frontend/               # Vue.js фронтенд
└── docs/                   # Документация
```

## Проверка работоспособности

После запуска проверьте:

1. **Health checks всех сервисов:**
   ```bash
   curl http://localhost:8000/healthz  # Orchestrator
   curl http://localhost:8001/healthz  # STT
   curl http://localhost:8004/healthz  # LLM
   curl http://localhost:8005/healthz  # Avatar
   curl http://localhost:3000          # Frontend
   ```

2. **MinIO bucket:**
   ```bash
   docker compose exec minio mc ls minio/audio-files
   ```

3. **API документация:**
   - Откройте http://localhost:8000/docs
   - Протестируйте эндпоинты

---

# 10) Переменные окружения

Создайте файл `.env` на основе `env.sample`:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@db:5432/interview_ai

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint

# MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET_NAME=audio-files
```

---

# 11) Разработка

## Добавление новых функций

1. **Backend изменения:**
   - Добавьте эндпоинты в соответствующий сервис
   - Обновите модели данных при необходимости
   - Добавьте тесты

2. **Frontend изменения:**
   - Обновите Vue компоненты
   - Добавьте новые страницы при необходимости
   - Обновите стили

3. **Пересборка:**
   ```bash
   docker compose build [service]
   docker compose up -d [service]
   ```

## Отладка

- **Логи сервисов:** `docker compose logs -f [service]`
- **База данных:** `docker compose exec db psql -U postgres -d interview_ai`
- **MinIO:** `docker compose exec minio mc ls minio/audio-files`

---

# 12) Безопасность

* Аудио файлы хранятся в MinIO с ограниченным доступом
* API ключи хранятся в переменных окружения
* Все сервисы изолированы в Docker контейнерах
* Health checks для мониторинга состояния

---

# 13) Поддержка

При возникновении проблем:

1. Проверьте логи сервисов
2. Убедитесь, что все контейнеры запущены
3. Проверьте переменные окружения
4. Создайте issue в репозитории

---

# 14) Лицензия

MIT License
