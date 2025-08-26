# Changelog

Все значимые изменения в проекте будут документированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и проект следует [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Added
- Базовая структура проекта с микросервисной архитектурой
- Docker Compose конфигурация для всех сервисов
- FastAPI приложения для всех сервисов (orchestrator, stt, tts, scoring)
- Vue.js фронтенд с Element Plus
- База данных PostgreSQL с полной схемой
- MinIO для хранения аудиофайлов
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

## [0.1.0] - 2025-01-15

### Added
- Инициализация проекта
- Базовая документация
- План разработки (TODOs.md)
