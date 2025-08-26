-- Initial database schema for Interview AI system

-- Candidates table
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    fio VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vacancies table
CREATE TABLE vacancies (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Questions table
CREATE TABLE questions (
    id VARCHAR(50) PRIMARY KEY,
    text TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'text',
    max_duration_s INTEGER DEFAULT 60,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criteria table
CREATE TABLE criteria (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vacancy questions junction table
CREATE TABLE vacancy_questions (
    vacancy_id VARCHAR(50) REFERENCES vacancies(id) ON DELETE CASCADE,
    question_id VARCHAR(50) REFERENCES questions(id) ON DELETE CASCADE,
    step_no INTEGER NOT NULL,
    question_weight DECIMAL(3,2) DEFAULT 1.0,
    must_have BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (vacancy_id, question_id)
);

-- Question criteria junction table
CREATE TABLE question_criteria (
    question_id VARCHAR(50) REFERENCES questions(id) ON DELETE CASCADE,
    criterion_id VARCHAR(50) REFERENCES criteria(id) ON DELETE CASCADE,
    weight DECIMAL(3,2) DEFAULT 1.0,
    must_have BOOLEAN DEFAULT FALSE,
    min_score DECIMAL(3,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (question_id, criterion_id)
);

-- Sessions table
CREATE TABLE sessions (
    id VARCHAR(50) PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE SET NULL,
    vacancy_id VARCHAR(50) REFERENCES vacancies(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'created',
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    total_score DECIMAL(3,2),
    current_step INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Q&A table
CREATE TABLE qa (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50) REFERENCES sessions(id) ON DELETE CASCADE,
    step_no INTEGER NOT NULL,
    question_id VARCHAR(50) REFERENCES questions(id) ON DELETE SET NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT,
    audio_url VARCHAR(500),
    tone VARCHAR(50),
    passed BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Q&A scores table
CREATE TABLE qa_scores (
    id SERIAL PRIMARY KEY,
    qa_id INTEGER REFERENCES qa(id) ON DELETE CASCADE,
    criterion_id VARCHAR(50) REFERENCES criteria(id) ON DELETE SET NULL,
    score DECIMAL(3,2) NOT NULL,
    evidence TEXT,
    red_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Media files table
CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50) REFERENCES sessions(id) ON DELETE CASCADE,
    kind VARCHAR(50) NOT NULL, -- 'question_audio', 'answer_audio'
    url VARCHAR(500) NOT NULL,
    duration_ms INTEGER,
    file_size_bytes BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_sessions_candidate_id ON sessions(candidate_id);
CREATE INDEX idx_sessions_vacancy_id ON sessions(vacancy_id);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_qa_session_id ON qa(session_id);
CREATE INDEX idx_qa_scores_qa_id ON qa_scores(qa_id);
CREATE INDEX idx_media_session_id ON media(session_id);
CREATE INDEX idx_vacancy_questions_vacancy_id ON vacancy_questions(vacancy_id);
CREATE INDEX idx_question_criteria_question_id ON question_criteria(question_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vacancies_updated_at BEFORE UPDATE ON vacancies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON questions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_criteria_updated_at BEFORE UPDATE ON criteria FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_qa_updated_at BEFORE UPDATE ON qa FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_qa_scores_updated_at BEFORE UPDATE ON qa_scores FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
