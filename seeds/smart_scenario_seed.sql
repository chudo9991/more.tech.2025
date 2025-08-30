-- Seed data for smart interview scenarios

-- Create smart scenario for Backend Developer
INSERT INTO interview_scenarios (id, vacancy_id, name, description, is_active, version) VALUES
('SCENARIO_BACKEND_001', 'SWE_BACK_001', 'Smart Backend Developer Interview', 'Адаптивный сценарий для интервью Backend Developer с умной навигацией', true, '1.0');

-- Create scenario nodes
INSERT INTO scenario_nodes (id, scenario_id, question_id, node_type, position_x, position_y, node_config) VALUES
-- Start node
('NODE_START_001', 'SCENARIO_BACKEND_001', NULL, 'start', 100, 100, '{"label": "Начало интервью"}'),

-- Question nodes
('NODE_FASTAPI_001', 'SCENARIO_BACKEND_001', 'Q_FASTAPI_01', 'question', 300, 100, '{"label": "FastAPI Experience", "weight": 1.0, "must_have": true}'),
('NODE_ASYNCIO_001', 'SCENARIO_BACKEND_001', 'Q_ASYNCIO_01', 'question', 500, 100, '{"label": "Async Programming", "weight": 0.8, "must_have": false}'),
('NODE_DATABASE_001', 'SCENARIO_BACKEND_001', 'Q_DATABASE_01', 'question', 700, 100, '{"label": "Database Experience", "weight": 0.9, "must_have": false}'),
('NODE_TESTING_001', 'SCENARIO_BACKEND_001', 'Q_TESTING_01', 'question', 900, 100, '{"label": "Testing Approach", "weight": 0.7, "must_have": false}'),
('NODE_MICROSERVICES_001', 'SCENARIO_BACKEND_001', 'Q_MICROSERVICES_01', 'question', 1100, 100, '{"label": "Microservices", "weight": 0.8, "must_have": false}'),
('NODE_DEPLOYMENT_001', 'SCENARIO_BACKEND_001', 'Q_DEPLOYMENT_01', 'question', 1300, 100, '{"label": "Deployment", "weight": 0.6, "must_have": false}'),
('NODE_PROBLEM_SOLVING_001', 'SCENARIO_BACKEND_001', 'Q_PROBLEM_SOLVING_01', 'question', 1500, 100, '{"label": "Problem Solving", "weight": 0.9, "must_have": false}'),
('NODE_TEAMWORK_001', 'SCENARIO_BACKEND_001', 'Q_TEAMWORK_01', 'question', 1700, 100, '{"label": "Teamwork", "weight": 0.7, "must_have": false}'),

-- Skip nodes for negative responses
('NODE_SKIP_PYTHON_001', 'SCENARIO_BACKEND_001', NULL, 'skip', 500, 300, '{"label": "Skip Python Questions", "skip_reason": "negative_fastapi_response"}'),
('NODE_SKIP_ADVANCED_001', 'SCENARIO_BACKEND_001', NULL, 'skip', 1100, 300, '{"label": "Skip Advanced Topics", "skip_reason": "low_basic_skills"}'),

-- End node
('NODE_END_001', 'SCENARIO_BACKEND_001', NULL, 'end', 1900, 100, '{"label": "Завершение интервью"}');

-- Create scenario transitions
INSERT INTO scenario_transitions (id, scenario_id, from_node_id, to_node_id, condition_type, condition_value, priority, transition_label) VALUES
-- Start transitions
('TRANS_START_FASTAPI', 'SCENARIO_BACKEND_001', 'NODE_START_001', 'NODE_FASTAPI_001', 'always', '{}', 1, 'Начать с FastAPI'),

-- FastAPI transitions
('TRANS_FASTAPI_ASYNCIO', 'SCENARIO_BACKEND_001', 'NODE_FASTAPI_001', 'NODE_ASYNCIO_001', 'score_threshold', '{"min_score": 0.3, "criterion": "FASTAPI"}', 1, 'Продолжить с Async'),
('TRANS_FASTAPI_SKIP', 'SCENARIO_BACKEND_001', 'NODE_FASTAPI_001', 'NODE_SKIP_PYTHON_001', 'score_threshold', '{"max_score": 0.3, "criterion": "FASTAPI"}', 2, 'Пропустить Python вопросы'),
('TRANS_FASTAPI_NEGATIVE', 'SCENARIO_BACKEND_001', 'NODE_FASTAPI_001', 'NODE_SKIP_PYTHON_001', 'negative_response', '{"patterns": ["не знаю", "не работал", "не знаком", "не использовал"]}', 3, 'Отрицательный ответ'),

-- Async transitions
('TRANS_ASYNCIO_DATABASE', 'SCENARIO_BACKEND_001', 'NODE_ASYNCIO_001', 'NODE_DATABASE_001', 'always', '{}', 1, 'Перейти к БД'),

-- Database transitions
('TRANS_DATABASE_TESTING', 'SCENARIO_BACKEND_001', 'NODE_DATABASE_001', 'NODE_TESTING_001', 'always', '{}', 1, 'Перейти к тестированию'),

-- Testing transitions
('TRANS_TESTING_MICROSERVICES', 'SCENARIO_BACKEND_001', 'NODE_TESTING_001', 'NODE_MICROSERVICES_001', 'score_threshold', '{"min_score": 0.5, "criterion": "TESTING"}', 1, 'Продолжить с микросервисами'),
('TRANS_TESTING_SKIP_ADVANCED', 'SCENARIO_BACKEND_001', 'NODE_TESTING_001', 'NODE_SKIP_ADVANCED_001', 'score_threshold', '{"max_score": 0.5, "criterion": "TESTING"}', 2, 'Пропустить продвинутые темы'),

-- Microservices transitions
('TRANS_MICROSERVICES_DEPLOYMENT', 'SCENARIO_BACKEND_001', 'NODE_MICROSERVICES_001', 'NODE_DEPLOYMENT_001', 'always', '{}', 1, 'Перейти к деплою'),

-- Deployment transitions
('TRANS_DEPLOYMENT_PROBLEM_SOLVING', 'SCENARIO_BACKEND_001', 'NODE_DEPLOYMENT_001', 'NODE_PROBLEM_SOLVING_001', 'always', '{}', 1, 'Перейти к решению проблем'),

-- Problem Solving transitions
('TRANS_PROBLEM_SOLVING_TEAMWORK', 'SCENARIO_BACKEND_001', 'NODE_PROBLEM_SOLVING_001', 'NODE_TEAMWORK_001', 'always', '{}', 1, 'Перейти к командной работе'),

-- Teamwork transitions
('TRANS_TEAMWORK_END', 'SCENARIO_BACKEND_001', 'NODE_TEAMWORK_001', 'NODE_END_001', 'always', '{}', 1, 'Завершить интервью'),

-- Skip transitions
('TRANS_SKIP_PYTHON_DATABASE', 'SCENARIO_BACKEND_001', 'NODE_SKIP_PYTHON_001', 'NODE_DATABASE_001', 'always', '{}', 1, 'Перейти к БД (пропустив Python)'),
('TRANS_SKIP_ADVANCED_PROBLEM_SOLVING', 'SCENARIO_BACKEND_001', 'NODE_SKIP_ADVANCED_001', 'NODE_PROBLEM_SOLVING_001', 'always', '{}', 1, 'Перейти к решению проблем (пропустив продвинутые темы)'),

-- Early termination transitions
('TRANS_FASTAPI_END_EARLY', 'SCENARIO_BACKEND_001', 'NODE_FASTAPI_001', 'NODE_END_001', 'negative_response', '{"patterns": ["не знаю программирование", "не разработчик", "не технический"], "terminate": true}', 4, 'Завершить досрочно');
