# Changelog

Все значимые изменения в проекте будут документированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и проект следует [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Added
- **Расширенная система вакансий с полями из BA.docx**
  - Добавлены все поля из таблицы требований к кандидату
  - Автоматическая генерация уникальных кодов вакансий (формат: ABBREVIATION-YEAR-NUMBER)
  - Полный CRUD API для управления вакансиями
  - Фильтрация и поиск вакансий
  - Статистика по вакансиям
  - Индексы для оптимизации поиска
- **Веб-интерфейс для управления вакансиями**
  - Современный UI с использованием Vue.js и Element Plus
  - Страница списка вакансий с фильтрацией и поиском
  - Форма создания/редактирования вакансий с валидацией
  - Детальная страница просмотра вакансии
  - Статистические карточки и пагинация
  - Интеграция с API через nginx прокси
- **Интеграция системы вакансий с HR-панелью**
  - Обновлена HR-панель для работы с новой системой вакансий
  - Добавлена фильтрация сессий по вакансиям с отображением кодов
  - Улучшенный UI с иконками и статистическими карточками
  - Компонент создания новых сессий с выбором вакансии
  - Предварительный просмотр деталей вакансии при создании сессии
  - Автоматическое заполнение vacancy_code в сессиях
  - Обновленные схемы данных для поддержки vacancy_code
- **Интеграция системы вакансий с процессом интервью**
  - Обновлена модель Question для поддержки специфичных для вакансий вопросов
  - Добавлены поля is_vacancy_specific, category, difficulty_level
  - Интегрированы требования вакансии в процесс интервью
  - Добавлен контекст вакансии в вопросы интервью
  - Обновлен интерфейс интервью с отображением информации о вакансии
  - Создан API endpoint для получения следующего вопроса с контекстом
  - Улучшена логика выбора вопросов на основе vacancy_questions
  - Добавлена поддержка весов вопросов и обязательных критериев
- Базовая структура проекта с микросервисной архитектурой
- Docker Compose конфигурация для всех сервисов
- FastAPI приложения для всех сервисов (orchestrator, stt, llm, avatar, scoring)
- Vue.js фронтенд с Element Plus
- База данных PostgreSQL с полной схемой
- MinIO для хранения аудиофайлов и аватаров
- Makefile с командами для управления проектом
- Демо-данные для тестирования
- Структурированное логирование
- Health check эндпоинты для всех сервисов
- Конфигурационные файлы для всех сервисов
- API роутеры и эндпоинты
- Многоконтейнерные Dockerfile'ы с оптимизацией размера
- Nginx конфигурация для фронтенда
- Система миграций базы данных (Alembic)
- Семплинг переменных окружения
- SQLAlchemy модели для всех сущностей
- Pydantic схемы для API
- Бизнес-логика сервисов (SessionService, WebhookService, HRService)
- ER-диаграмма базы данных
- Скрипты для загрузки демо-данных

### Changed
- **Архитектурные изменения:**
  - Заменен TTS сервис на LLM сервис с Azure GPT-4o интеграцией
  - Добавлен Avatar сервис для генерации AI-аватаров
  - Изменен flow общения: веб-интерфейс вместо телефонных звонков
  - Добавлен интерфейс для кандидатов с голосовым общением
  - Обновлена навигация и роутинг фронтенда
  - Обновлены конфигурации и переменные окружения

#### Phase D1 - Ядро интервью
- **T-10: Orchestrator: сессии и шаги**
  - Enhanced session management endpoints
  - Improved session service with proper error handling
  - Updated API schemas for session operations
  - Fixed webhook service imports and functionality

- **T-11: SIP-вебхуки и симулятор провайдера**
  - SIP webhook endpoints for call events
  - Record webhook endpoints for audio processing
  - SIP provider simulator for testing
  - Webhook service with proper event handling

- **T-12: STT + VAD**
  - Whisper-based transcription service
  - Voice Activity Detection (VAD) integration
  - Paralinguistic feature extraction
  - Audio processing with librosa and pydub
  - Enhanced STT configuration with VAD settings

- **T-13: TTS + кэш**
  - TTS service with multiple model support
  - Audio caching system for performance
  - Speech synthesis with configurable voices
  - Audio file management and storage

- **T-14: Scoring (LLM) — строгий JSON**
  - LLM-based answer scoring service
  - Strict JSON response validation
  - Support for OpenAI and Anthropic APIs
  - Criterion-based scoring with evidence
  - JSON repair mechanisms for malformed responses

- **T-15: Tone & паралингвистика**
  - Tone analysis service (positive/neutral/negative)
  - Paralinguistic feature analysis
  - Confidence indicator analysis
  - Text-based speech rate estimation
  - Multilingual tone detection

- **T-16: Сохранение результатов и агрегация**
  - Enhanced session service with full pipeline integration
  - Automatic transcription and scoring workflow
  - Session results aggregation and statistics
  - Export service for reports (JSON, CSV, Summary)
  - Vacancy-level reporting and analytics
  - Session progress tracking and completion status

- **T-17: Frontend HR-панель**
  - Complete HR panel interface with Vue.js and Element Plus
  - Session management dashboard with statistics and filtering
  - Detailed session view with questions, answers, and scores
  - Export functionality for individual sessions and vacancies
  - Pinia store for state management
  - Responsive design with modern UI components
  - Audio playback for interview recordings
  - Performance analytics and improvement suggestions

- **T-18: Экспорт и отчеты**
  - Enhanced export service with multiple formats (JSON, CSV, PDF, HTML)
  - Professional PDF reports with structured layouts and styling
  - HTML reports with responsive design and modern styling
  - Session-level and vacancy-level reporting
  - Detailed question analysis with metrics and scores
  - Performance summaries and improvement suggestions
  - Timestamped exports with proper file naming

- **T-19: Мониторинг и логирование**
  - Comprehensive monitoring service with system health checks
  - Session metrics tracking with time-based analytics
  - Performance alerts and error rate monitoring
  - Structured logging with event tracking
  - Database health monitoring and service metrics
  - Export functionality for monitoring reports
  - Real-time performance monitoring and alerting

- **T-20: Финальная полировка**
  - Complete demo script for end-to-end system testing
  - Enhanced Makefile with comprehensive commands
  - Updated documentation with final instructions
  - System integration testing and validation
  - Performance optimization and error handling
  - Production-ready deployment configuration
  - Comprehensive testing suite and validation

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## [1.0.0] - 2025-08-27

### Added
- **Новый модуль LLM (Azure GPT-4o)**
  - Интеграция с Azure OpenAI для анализа ответов
  - Анализ тона голоса и эмоционального состояния
  - Генерация ответов аватара
  - Строгая валидация JSON ответов

- **Новый модуль Avatar**
  - Заглушка для RTSP потока AI-аватара
  - Подготовлена архитектура для интеграции с внешними сервисами
  - Динамическое изменение эмоций аватара

- **Веб-интерфейс для кандидатов**
  - Полноценный интерфейс интервью с голосовым общением
  - Voice Activity Detection (VAD) для автоматической остановки записи
  - Web Audio API для записи аудио в браузере
  - Кнопки "Ответ" и "Стоп" для управления записью
  - Автоматическая обработка аудио через STT

- **Интеграция MinIO**
  - S3-совместимое хранилище для аудио файлов
  - Автоматическое создание bucket'ов
  - Безопасное хранение и доступ к аудио записям
  - Воспроизведение аудио в HR панели

- **Анализ тона голоса**
  - Детальный анализ эмоционального состояния кандидата
  - Классификация тона: positive/neutral/concerned/excited/confused/confident
  - Отображение результатов в HR панели с эмодзи
  - Сохранение анализа в базе данных

- **Обновленная HR панель**
  - Воспроизведение аудио записей интервью
  - Отображение анализа тона голоса
  - Детальная информация о транскрипции
  - Улучшенный интерфейс с русским языком

- **Voice Activity Detection (VAD)**
  - Автоматическая остановка записи по тишине
  - Настраиваемые параметры: VAD_VOLUME_THRESHOLD, VAD_SILENCE_THRESHOLD
  - Интеграция с webrtcvad для точного определения речи
  - Оптимизация для русского языка

### Changed
- **Архитектурная переработка**
  - Удален TTS модуль, заменен на голосовое общение через веб
  - Изменен flow общения: веб-интерфейс вместо телефонных звонков
  - Обновлена микросервисная архитектура
  - Переход на Azure GPT-4o для LLM функциональности

- **Frontend обновления**
  - Полный перевод интерфейса на русский язык
  - Новая навигация с кнопкой "Начать интервью"
  - Удалены ненужные элементы интерфейса (текстовый ввод, текущий балл)
  - Улучшенный UX для голосового общения

- **Backend улучшения**
  - Обновлены модели данных для поддержки анализа тона
  - Улучшена обработка аудио файлов
  - Добавлена поддержка MinIO клиента в orchestrator
  - Исправлены проблемы с асинхронным программированием

- **Конфигурация и развертывание**
  - Обновлен docker-compose.yml для новых сервисов
  - Добавлены переменные окружения для Azure OpenAI
  - Улучшена конфигурация MinIO
  - Обновлены health checks

### Removed
- **TTS модуль**
  - Полностью удален модуль синтеза речи
  - Удалены все связанные файлы и конфигурации
  - Заменен на веб-интерфейс с голосовым общением

- **Устаревшие элементы интерфейса**
  - Текстовый ввод в интерфейсе интервью
  - Отображение текущего балла
  - Кнопка "Generate Avatar" (заменена на RTSP заглушку)

### Fixed
- **Проблемы с воспроизведением аудио**
  - Исправлена интеграция с MinIO для получения аудио файлов
  - Заменен boto3 на minio клиент в orchestrator
  - Исправлена обработка имен файлов с специальными символами
  - Добавлена корректная обработка ошибок 404

- **Voice Activity Detection**
  - Исправлены параметры VAD для корректной работы
  - Оптимизированы настройки тишины и громкости
  - Улучшена стабильность автоматической остановки записи

- **Интеграция сервисов**
  - Исправлены проблемы с асинхронным программированием
  - Улучшена обработка ошибок между сервисами
  - Исправлены проблемы с роутингом API

- **Frontend ошибки**
  - Убрана ошибка 404 для vite.svg
  - Исправлена видимость кнопок управления записью
  - Улучшена обработка ошибок воспроизведения аудио

### Security
- Обновлены переменные окружения для безопасного хранения API ключей
- Улучшена изоляция сервисов в Docker контейнерах
- Добавлены health checks для мониторинга состояния

---

## [0.1.0] - 2025-01-15

### Added
- Инициализация проекта
- Базовая документация
- План разработки (TODOs.md)
