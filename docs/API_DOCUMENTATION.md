# 📚 API Documentation - Resume System

## Обзор

Система управления резюме предоставляет REST API для загрузки, обработки и анализа резюме кандидатов. API поддерживает различные форматы файлов, batch обработку и интеграцию с системой вакансий.

## Базовый URL

```
http://localhost:8000/api/v1
```

## Аутентификация

В текущей версии API не требует аутентификации. В продакшене рекомендуется использовать JWT токены.

## Общие заголовки

```
Content-Type: application/json
Accept: application/json
```

## Endpoints

### 📄 Resume Management

#### Получить список резюме

```http
GET /resumes
```

**Query Parameters:**
- `skip` (int, optional): Количество записей для пропуска (по умолчанию: 0)
- `limit` (int, optional): Максимальное количество записей (по умолчанию: 25)
- `status` (string, optional): Фильтр по статусу (uploaded, processing, analyzed, error)
- `vacancy_id` (string, optional): Фильтр по ID вакансии
- `sort_by` (string, optional): Поле для сортировки (upload_date, total_score, confidence_score)
- `sort_order` (string, optional): Порядок сортировки (asc, desc)

**Response:**
```json
{
  "resumes": [
    {
      "id": "resume_001",
      "filename": "resume.pdf",
      "original_filename": "my_resume.pdf",
      "file_type": "pdf",
      "file_size": 1024,
      "status": "analyzed",
      "total_score": 85.5,
      "confidence_score": 0.9,
      "upload_date": "2024-01-01T10:00:00Z",
      "vacancy_id": "vacancy_001",
      "vacancy_title": "Backend Developer"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 25,
  "total_pages": 4
}
```

#### Получить резюме по ID

```http
GET /resumes/{resume_id}
```

**Response:**
```json
{
  "id": "resume_001",
  "filename": "resume.pdf",
  "original_filename": "my_resume.pdf",
  "file_type": "pdf",
  "file_size": 1024,
  "status": "analyzed",
  "total_score": 85.5,
  "confidence_score": 0.9,
  "upload_date": "2024-01-01T10:00:00Z",
  "vacancy_id": "vacancy_001",
  "vacancy_title": "Backend Developer",
  "resume_blocks": [
    {
      "id": "block_001",
      "block_type": "experience",
      "block_name": "Work Experience",
      "extracted_text": "Senior Developer at Tech Corp...",
      "relevance_score": 0.9,
      "confidence_score": 0.85,
      "matched_requirements": ["Python", "Django"],
      "missing_requirements": ["Kubernetes"],
      "analysis_notes": "Strong backend experience"
    }
  ],
  "resume_skills": [
    {
      "id": "skill_001",
      "skill_name": "Python",
      "category": "programming",
      "experience_level": "expert",
      "confidence_score": 0.95
    }
  ]
}
```

#### Загрузить резюме

```http
POST /resumes/upload
```

**Request (multipart/form-data):**
- `file`: Файл резюме (PDF, DOCX, RTF, TXT)
- `vacancy_id` (string, optional): ID вакансии для привязки
- `vacancy_code` (string, optional): Код вакансии для привязки

**Response:**
```json
{
  "id": "resume_001",
  "filename": "resume_20240101_120000.pdf",
  "original_filename": "my_resume.pdf",
  "file_type": "pdf",
  "file_size": 1024,
  "status": "uploaded",
  "upload_date": "2024-01-01T12:00:00Z"
}
```

#### Обработать резюме

```http
POST /resumes/{resume_id}/process
```

**Response:**
```json
{
  "success": true,
  "resume_id": "resume_001",
  "sections_found": 5,
  "skills_found": 12,
  "experience_years": 3,
  "education_level": "bachelor"
}
```

#### Рассчитать оценку релевантности

```http
POST /resumes/{resume_id}/calculate-score
```

**Response:**
```json
{
  "success": true,
  "resume_id": "resume_001",
  "total_score": 85.5,
  "confidence_score": 0.9,
  "cached": false
}
```

#### Удалить резюме

```http
DELETE /resumes/{resume_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Resume deleted successfully"
}
```

#### Получить статистику резюме

```http
GET /resumes/statistics
```

**Response:**
```json
{
  "total_resumes": 100,
  "processed_resumes": 85,
  "error_resumes": 5,
  "average_score": 75.5,
  "score_distribution": {
    "excellent": 20,
    "good": 35,
    "average": 25,
    "poor": 5
  },
  "top_vacancies": [
    {
      "vacancy_id": "vacancy_001",
      "vacancy_code": "BACKEND_001",
      "title": "Backend Developer",
      "count": 25
    }
  ]
}
```

### 📦 Batch Processing

#### Пакетная загрузка резюме

```http
POST /batch/upload
```

**Request (multipart/form-data):**
- `files[]`: Массив файлов резюме (до 50 файлов)
- `vacancy_id` (string, optional): ID вакансии для привязки
- `max_concurrent` (int, optional): Максимум одновременных операций (1-10, по умолчанию: 3)

**Response:**
```json
{
  "batch_id": "batch_20240101_120000",
  "status": "completed",
  "total_files": 5,
  "successful": 4,
  "failed": 1,
  "processing_time_seconds": 45.2,
  "results": [
    {
      "file_index": 0,
      "filename": "resume1.pdf",
      "status": "success",
      "resume_id": "resume_001",
      "sections_found": 5,
      "skills_found": 12
    },
    {
      "file_index": 1,
      "filename": "resume2.pdf",
      "status": "error",
      "error": "File processing failed"
    }
  ]
}
```

#### Получить статус batch операции

```http
GET /batch/status/{batch_id}
```

**Response:**
```json
{
  "batch_id": "batch_20240101_120000",
  "status": "completed",
  "total_files": 5,
  "successful": 4,
  "failed": 1,
  "start_time": "2024-01-01T12:00:00Z",
  "end_time": "2024-01-01T12:00:45Z",
  "processing_time_seconds": 45.2,
  "results": [...]
}
```

#### Получить статистику batch операций

```http
GET /batch/statistics
```

**Response:**
```json
{
  "total_batches": 10,
  "successful_batches": 8,
  "failed_batches": 2,
  "average_processing_time": 30.5,
  "total_files_processed": 150
}
```

### 🔍 Monitoring

#### Проверка здоровья системы

```http
GET /monitoring/health
```

**Response:**
```json
{
  "status": "healthy",
  "cache_service": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Информация о кэше

```http
GET /monitoring/cache/info
```

**Response:**
```json
{
  "cache_info": {
    "resume_analysis": 25,
    "vacancy_requirements": 10,
    "resume_score": 50,
    "statistics": 5,
    "file_processing": 15,
    "total_keys": 105,
    "memory_usage": {
      "used_memory": "50MB",
      "total_memory": "1GB"
    }
  },
  "cache_healthy": true
}
```

#### Очистить кэш

```http
POST /monitoring/cache/clear
```

**Query Parameters:**
- `prefix` (string, optional): Префикс для очистки (если не указан, очищается весь кэш)

**Response:**
```json
{
  "success": true,
  "message": "Cleared all cache"
}
```

## Коды ошибок

### HTTP Status Codes

- `200 OK` - Успешный запрос
- `201 Created` - Ресурс создан
- `400 Bad Request` - Неверный запрос
- `404 Not Found` - Ресурс не найден
- `422 Unprocessable Entity` - Ошибка валидации
- `500 Internal Server Error` - Внутренняя ошибка сервера

### Примеры ошибок

```json
{
  "detail": "Resume not found"
}
```

```json
{
  "detail": "File too large (max 10MB)"
}
```

```json
{
  "detail": "Unsupported file format"
}
```

## Ограничения

### Файлы
- **Максимальный размер**: 10MB
- **Поддерживаемые форматы**: PDF, DOCX, RTF, TXT
- **Batch загрузка**: до 50 файлов за раз

### API
- **Rate limiting**: 100 запросов в минуту
- **Timeout**: 30 секунд для обработки файлов
- **Pagination**: максимум 100 записей на страницу

## Примеры использования

### cURL

#### Загрузка резюме
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/upload" \
  -F "file=@resume.pdf" \
  -F "vacancy_id=vacancy_001"
```

#### Batch загрузка
```bash
curl -X POST "http://localhost:8000/api/v1/batch/upload" \
  -F "files[]=@resume1.pdf" \
  -F "files[]=@resume2.pdf" \
  -F "vacancy_id=vacancy_001" \
  -F "max_concurrent=3"
```

#### Получение статистики
```bash
curl -X GET "http://localhost:8000/api/v1/resumes/statistics"
```

### JavaScript (Fetch)

#### Загрузка резюме
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('vacancy_id', 'vacancy_001');

const response = await fetch('/api/v1/resumes/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

#### Batch загрузка
```javascript
const formData = new FormData();
files.forEach(file => {
  formData.append('files[]', file);
});
formData.append('vacancy_id', 'vacancy_001');
formData.append('max_concurrent', '3');

const response = await fetch('/api/v1/batch/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

## Версионирование

API использует семантическое версионирование. Текущая версия: `v1`

Изменения в API будут сопровождаться увеличением номера версии и соответствующей документацией.

## Поддержка

Для получения поддержки или сообщения об ошибках, пожалуйста, создайте issue в репозитории проекта.
