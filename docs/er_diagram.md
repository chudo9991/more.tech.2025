# ER Diagram - Interview AI Database

## Entity Relationship Diagram

```mermaid
erDiagram
    CANDIDATES {
        int id PK
        string fio
        string phone
        string email
        datetime created_at
        datetime updated_at
    }

    VACANCIES {
        string id PK
        string title
        text description
        datetime created_at
        datetime updated_at
    }

    QUESTIONS {
        string id PK
        text text
        string type
        int max_duration_s
        datetime created_at
        datetime updated_at
    }

    CRITERIA {
        string id PK
        string code UK
        string name
        text description
        datetime created_at
        datetime updated_at
    }

    SESSIONS {
        string id PK
        int candidate_id FK
        string vacancy_id FK
        string phone
        string email
        string status
        datetime started_at
        datetime finished_at
        decimal total_score
        decimal pass_rate
        int current_step
        int total_steps
        datetime created_at
        datetime updated_at
    }

    MESSAGES {
        string id PK
        string session_id FK
        text text
        string message_type
        string audio_url
        int transcription_confidence
        datetime timestamp
        datetime created_at
    }

    QA {
        int id PK
        string session_id FK
        int step_no
        string question_id FK
        text question_text
        text answer_text
        string audio_url
        string tone
        boolean passed
        datetime created_at
        datetime updated_at
    }

    QA_SCORES {
        int id PK
        int qa_id FK
        string criterion_id FK
        decimal score
        text evidence
        boolean red_flag
        datetime created_at
        datetime updated_at
    }

    MEDIA {
        int id PK
        string session_id FK
        string kind
        string url
        int duration_ms
        bigint file_size_bytes
        datetime created_at
    }

    VACANCY_QUESTIONS {
        string vacancy_id FK,PK
        string question_id FK,PK
        int step_no
        decimal question_weight
        boolean must_have
        datetime created_at
    }

    QUESTION_CRITERIA {
        string question_id FK,PK
        string criterion_id FK,PK
        decimal weight
        boolean must_have
        decimal min_score
        datetime created_at
    }

    CANDIDATES ||--o{ SESSIONS : "has"
    VACANCIES ||--o{ SESSIONS : "has"
    SESSIONS ||--o{ MESSAGES : "contains"
    SESSIONS ||--o{ QA : "contains"
    SESSIONS ||--o{ MEDIA : "has"
    QUESTIONS ||--o{ QA : "asked_in"
    QA ||--o{ QA_SCORES : "evaluated_by"
    CRITERIA ||--o{ QA_SCORES : "used_in"
    VACANCIES ||--o{ VACANCY_QUESTIONS : "includes"
    QUESTIONS ||--o{ VACANCY_QUESTIONS : "included_in"
    QUESTIONS ||--o{ QUESTION_CRITERIA : "evaluated_by"
    CRITERIA ||--o{ QUESTION_CRITERIA : "used_for"
```

## Table Descriptions

### Core Entities

- **CANDIDATES**: People who participate in interviews
- **VACANCIES**: Job positions being interviewed for
- **QUESTIONS**: Interview questions with metadata
- **CRITERIA**: Evaluation criteria for scoring answers

### Interview Process

- **SESSIONS**: Individual interview sessions linking candidates to vacancies
- **MESSAGES**: Chat messages within a session (both user and avatar messages)
- **QA**: Question-Answer pairs within a session
- **QA_SCORES**: Detailed scoring of answers against criteria
- **MEDIA**: Audio files for questions and answers

### Configuration

- **VACANCY_QUESTIONS**: Links questions to vacancies with ordering and weights
- **QUESTION_CRITERIA**: Links criteria to questions with weights and requirements

## Key Features

1. **Flexible Question-Criteria Mapping**: Each question can be evaluated against multiple criteria with different weights
2. **Must-Have Requirements**: Questions and criteria can be marked as required for passing
3. **Audio Support**: Full audio file management for questions and answers
4. **Session Tracking**: Complete interview session lifecycle management
5. **Detailed Scoring**: Granular scoring with evidence and red flags
6. **Chat Messages**: Support for storing conversation messages with audio URLs and transcription confidence
7. **Session Metadata**: Direct phone and email storage in sessions for quick access
