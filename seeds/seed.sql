-- Seed data for Interview AI system

-- Insert demo candidates
INSERT INTO candidates (fio, phone, email) VALUES
('Иванов Иван Иванович', '+7-999-123-45-67', 'ivanov@example.com'),
('Петрова Анна Сергеевна', '+7-999-234-56-78', 'petrova@example.com'),
('Сидоров Алексей Петрович', '+7-999-345-67-89', 'sidorov@example.com');

-- Insert demo vacancy
INSERT INTO vacancies (id, title, description) VALUES
('SWE_BACK_001', 'Backend Developer (Python)', 'Разработчик бэкенда на Python с опытом работы с FastAPI, PostgreSQL и микросервисной архитектурой');

-- Insert demo questions
INSERT INTO questions (id, text, type, max_duration_s) VALUES
('Q_FASTAPI_01', 'Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?', 'text', 120),
('Q_ASYNCIO_01', 'Объясните, как работает асинхронное программирование в Python. Приведите примеры использования asyncio.', 'text', 90),
('Q_DATABASE_01', 'Опишите ваш опыт работы с базами данных. Какие СУБД вы использовали и в каких проектах?', 'text', 100),
('Q_TESTING_01', 'Расскажите о вашем подходе к тестированию кода. Какие виды тестов вы пишете?', 'text', 80),
('Q_MICROSERVICES_01', 'Каков ваш опыт работы с микросервисной архитектурой? Какие проблемы вы решали?', 'text', 110),
('Q_DEPLOYMENT_01', 'Опишите процесс деплоя приложений. Какие инструменты и технологии вы используете?', 'text', 90),
('Q_PROBLEM_SOLVING_01', 'Опишите сложную техническую задачу, которую вам приходилось решать. Как вы подходили к её решению?', 'text', 120),
('Q_TEAMWORK_01', 'Расскажите о вашем опыте работы в команде. Как вы взаимодействуете с коллегами?', 'text', 100);

-- Insert demo criteria
INSERT INTO criteria (id, code, name, description) VALUES
('FASTAPI', 'FASTAPI', 'Опыт с FastAPI', 'Знание и опыт использования FastAPI фреймворка'),
('ASYNCIO', 'ASYNCIO', 'Асинхронное программирование', 'Понимание и опыт работы с asyncio'),
('DATABASE', 'DATABASE', 'Работа с БД', 'Опыт работы с различными базами данных'),
('TESTING', 'TESTING', 'Тестирование', 'Подход к тестированию кода'),
('MICROSERVICES', 'MICROSERVICES', 'Микросервисы', 'Опыт работы с микросервисной архитектурой'),
('DEPLOYMENT', 'DEPLOYMENT', 'Деплой', 'Опыт деплоя приложений'),
('PROBLEM_SOLVING', 'PROBLEM_SOLVING', 'Решение проблем', 'Способность решать сложные технические задачи'),
('TEAMWORK', 'TEAMWORK', 'Командная работа', 'Опыт работы в команде');

-- Link questions to vacancy
INSERT INTO vacancy_questions (vacancy_id, question_id, step_no, question_weight, must_have) VALUES
('SWE_BACK_001', 'Q_FASTAPI_01', 1, 1.0, TRUE),
('SWE_BACK_001', 'Q_ASYNCIO_01', 2, 0.8, FALSE),
('SWE_BACK_001', 'Q_DATABASE_01', 3, 0.9, FALSE),
('SWE_BACK_001', 'Q_TESTING_01', 4, 0.7, FALSE),
('SWE_BACK_001', 'Q_MICROSERVICES_01', 5, 0.8, FALSE),
('SWE_BACK_001', 'Q_DEPLOYMENT_01', 6, 0.6, FALSE),
('SWE_BACK_001', 'Q_PROBLEM_SOLVING_01', 7, 0.9, FALSE),
('SWE_BACK_001', 'Q_TEAMWORK_01', 8, 0.7, FALSE);

-- Link criteria to questions
INSERT INTO question_criteria (question_id, criterion_id, weight, must_have, min_score) VALUES
('Q_FASTAPI_01', 'FASTAPI', 0.8, TRUE, 0.7),
('Q_FASTAPI_01', 'ASYNCIO', 0.2, FALSE, 0.0),
('Q_ASYNCIO_01', 'ASYNCIO', 1.0, FALSE, 0.0),
('Q_DATABASE_01', 'DATABASE', 1.0, FALSE, 0.0),
('Q_TESTING_01', 'TESTING', 1.0, FALSE, 0.0),
('Q_MICROSERVICES_01', 'MICROSERVICES', 0.7, FALSE, 0.0),
('Q_MICROSERVICES_01', 'PROBLEM_SOLVING', 0.3, FALSE, 0.0),
('Q_DEPLOYMENT_01', 'DEPLOYMENT', 1.0, FALSE, 0.0),
('Q_PROBLEM_SOLVING_01', 'PROBLEM_SOLVING', 0.8, FALSE, 0.0),
('Q_PROBLEM_SOLVING_01', 'TEAMWORK', 0.2, FALSE, 0.0),
('Q_TEAMWORK_01', 'TEAMWORK', 1.0, FALSE, 0.0);

-- Insert demo session
INSERT INTO sessions (id, candidate_id, vacancy_id, status, started_at, finished_at, total_score, current_step) VALUES
('SESS_001', 1, 'SWE_BACK_001', 'completed', '2025-01-15 10:00:00+00', '2025-01-15 10:25:00+00', 0.82, 8);

-- Insert demo Q&A records
INSERT INTO qa (session_id, step_no, question_id, question_text, answer_text, audio_url, tone, passed) VALUES
('SESS_001', 1, 'Q_FASTAPI_01', 'Расскажите про ваш опыт работы с FastAPI...', 'Я работал с FastAPI в нескольких проектах. Использовал Depends для внедрения зависимостей, BackgroundTasks для асинхронных задач, Pydantic для валидации данных. Также интегрировал с PostgreSQL через SQLAlchemy.', 'https://minio:9000/interview-audio/answer_001.wav', 'positive', TRUE),
('SESS_001', 2, 'Q_ASYNCIO_01', 'Объясните, как работает асинхронное программирование...', 'Асинхронное программирование позволяет выполнять операции без блокировки. Использую async/await, asyncio.gather для параллельного выполнения задач.', 'https://minio:9000/interview-audio/answer_002.wav', 'neutral', TRUE),
('SESS_001', 3, 'Q_DATABASE_01', 'Опишите ваш опыт работы с базами данных...', 'Работал с PostgreSQL, Redis, MongoDB. Использую миграции, индексы для оптимизации запросов.', 'https://minio:9000/interview-audio/answer_003.wav', 'positive', TRUE),
('SESS_001', 4, 'Q_TESTING_01', 'Расскажите о вашем подходе к тестированию...', 'Пишу unit-тесты с pytest, интеграционные тесты, использую моки и фикстуры.', 'https://minio:9000/interview-audio/answer_004.wav', 'neutral', TRUE),
('SESS_001', 5, 'Q_MICROSERVICES_01', 'Каков ваш опыт работы с микросервисной архитектурой...', 'Работал с Docker, Kubernetes, сервис-мешами. Решал проблемы с сетевой связностью и мониторингом.', 'https://minio:9000/interview-audio/answer_005.wav', 'positive', TRUE),
('SESS_001', 6, 'Q_DEPLOYMENT_01', 'Опишите процесс деплоя приложений...', 'Использую CI/CD пайплайны, Docker контейнеры, автоматическое развертывание через GitLab CI.', 'https://minio:9000/interview-audio/answer_006.wav', 'neutral', TRUE),
('SESS_001', 7, 'Q_PROBLEM_SOLVING_01', 'Опишите сложную техническую задачу...', 'Оптимизировал медленные запросы к БД, использовал кэширование, переписал критические участки кода.', 'https://minio:9000/interview-audio/answer_007.wav', 'positive', TRUE),
('SESS_001', 8, 'Q_TEAMWORK_01', 'Расскажите о вашем опыте работы в команде...', 'Работаю в команде из 5 разработчиков, участвую в code review, помогаю коллегам с техническими вопросами.', 'https://minio:9000/interview-audio/answer_008.wav', 'positive', TRUE);

-- Insert demo scores for Q&A
INSERT INTO qa_scores (qa_id, criterion_id, score, evidence, red_flag) VALUES
(1, 'FASTAPI', 0.9, 'Упоминает Depends, BackgroundTasks, Pydantic - показывает глубокое знание фреймворка', FALSE),
(1, 'ASYNCIO', 0.7, 'Понимает асинхронность, но не показывает глубоких знаний', FALSE),
(2, 'ASYNCIO', 0.8, 'Правильно объясняет async/await, упоминает asyncio.gather', FALSE),
(3, 'DATABASE', 0.85, 'Опыт с разными БД, понимает миграции и индексы', FALSE),
(4, 'TESTING', 0.75, 'Знает pytest, понимает разные типы тестов', FALSE),
(5, 'MICROSERVICES', 0.8, 'Опыт с Docker, Kubernetes, понимает проблемы архитектуры', FALSE),
(5, 'PROBLEM_SOLVING', 0.7, 'Показывает способность решать технические проблемы', FALSE),
(6, 'DEPLOYMENT', 0.7, 'Знает CI/CD, Docker, автоматизацию', FALSE),
(7, 'PROBLEM_SOLVING', 0.9, 'Конкретный пример оптимизации с измеримыми результатами', FALSE),
(7, 'TEAMWORK', 0.6, 'Упоминает командную работу, но не детализирует', FALSE),
(8, 'TEAMWORK', 0.8, 'Конкретные примеры работы в команде, code review', FALSE);
