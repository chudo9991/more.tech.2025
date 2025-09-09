--
-- PostgreSQL database dump
--

\restrict EB9Hk4vyQk3x3BKW8ZbeFLT5BUXDzUnVhXXJafafngrmu2Meo5xCahlet9rKqHM

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS interview_ai;
--
-- Name: interview_ai; Type: DATABASE; Schema: -; Owner: interview_user
--

CREATE DATABASE interview_ai WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE interview_ai OWNER TO interview_user;

\unrestrict EB9Hk4vyQk3x3BKW8ZbeFLT5BUXDzUnVhXXJafafngrmu2Meo5xCahlet9rKqHM
\connect interview_ai
\restrict EB9Hk4vyQk3x3BKW8ZbeFLT5BUXDzUnVhXXJafafngrmu2Meo5xCahlet9rKqHM

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: sectiontype; Type: TYPE; Schema: public; Owner: interview_user
--

CREATE TYPE public.sectiontype AS ENUM (
    'RESPONSIBILITIES',
    'REQUIREMENTS',
    'PROGRAMS',
    'SKILLS',
    'LANGUAGES',
    'DESCRIPTION',
    'ADDITIONAL'
);


ALTER TYPE public.sectiontype OWNER TO interview_user;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: interview_user
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO interview_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO interview_user;

--
-- Name: candidates; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.candidates (
    id integer NOT NULL,
    fio character varying(255) NOT NULL,
    phone character varying(20),
    email character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.candidates OWNER TO interview_user;

--
-- Name: candidates_id_seq; Type: SEQUENCE; Schema: public; Owner: interview_user
--

CREATE SEQUENCE public.candidates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.candidates_id_seq OWNER TO interview_user;

--
-- Name: candidates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: interview_user
--

ALTER SEQUENCE public.candidates_id_seq OWNED BY public.candidates.id;


--
-- Name: contextual_questions; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.contextual_questions (
    id character varying(50) NOT NULL,
    session_id character varying(50) NOT NULL,
    scenario_node_id character varying(50) NOT NULL,
    question_text text NOT NULL,
    question_type character varying(50),
    context_source jsonb,
    generated_at timestamp with time zone DEFAULT now(),
    is_used boolean DEFAULT false,
    used_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.contextual_questions OWNER TO interview_user;

--
-- Name: criteria; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.criteria (
    id character varying(50) NOT NULL,
    code character varying(100) NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.criteria OWNER TO interview_user;

--
-- Name: dynamic_criteria; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.dynamic_criteria (
    id character varying(50) NOT NULL,
    vacancy_id character varying(50),
    skill_name character varying(255) NOT NULL,
    category character varying(100) NOT NULL,
    importance double precision DEFAULT 0.5 NOT NULL,
    required_level character varying(50) NOT NULL,
    is_mandatory boolean DEFAULT false,
    description character varying(500),
    alternatives json,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.dynamic_criteria OWNER TO interview_user;

--
-- Name: interview_codes; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.interview_codes (
    id character varying NOT NULL,
    code character varying(6) NOT NULL,
    resume_id character varying(50) NOT NULL,
    is_used boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    used_at timestamp with time zone
);


ALTER TABLE public.interview_codes OWNER TO interview_user;

--
-- Name: interview_scenarios; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.interview_scenarios (
    id character varying(50) NOT NULL,
    vacancy_id character varying(50),
    name character varying(255) NOT NULL,
    description text,
    is_active boolean,
    version character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.interview_scenarios OWNER TO interview_user;

--
-- Name: media; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.media (
    id integer NOT NULL,
    session_id character varying(50) NOT NULL,
    kind character varying(50) NOT NULL,
    url character varying(500) NOT NULL,
    duration_ms integer,
    file_size_bytes bigint,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.media OWNER TO interview_user;

--
-- Name: media_id_seq; Type: SEQUENCE; Schema: public; Owner: interview_user
--

CREATE SEQUENCE public.media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.media_id_seq OWNER TO interview_user;

--
-- Name: media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: interview_user
--

ALTER SEQUENCE public.media_id_seq OWNED BY public.media.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.messages (
    id character varying NOT NULL,
    session_id character varying NOT NULL,
    text text NOT NULL,
    message_type character varying NOT NULL,
    audio_url character varying,
    transcription_confidence integer,
    "timestamp" timestamp with time zone DEFAULT now(),
    created_at timestamp with time zone DEFAULT now(),
    tone_analysis character varying(50)
);


ALTER TABLE public.messages OWNER TO interview_user;

--
-- Name: qa; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.qa (
    id integer NOT NULL,
    session_id character varying(50) NOT NULL,
    step_no integer NOT NULL,
    question_id character varying(50),
    question_text text NOT NULL,
    answer_text text,
    audio_url character varying(500),
    tone character varying(50),
    passed boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.qa OWNER TO interview_user;

--
-- Name: qa_id_seq; Type: SEQUENCE; Schema: public; Owner: interview_user
--

CREATE SEQUENCE public.qa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qa_id_seq OWNER TO interview_user;

--
-- Name: qa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: interview_user
--

ALTER SEQUENCE public.qa_id_seq OWNED BY public.qa.id;


--
-- Name: qa_scores; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.qa_scores (
    id integer NOT NULL,
    qa_id integer NOT NULL,
    criterion_id character varying(50),
    score numeric(3,2) NOT NULL,
    evidence text,
    red_flag boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.qa_scores OWNER TO interview_user;

--
-- Name: qa_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: interview_user
--

CREATE SEQUENCE public.qa_scores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qa_scores_id_seq OWNER TO interview_user;

--
-- Name: qa_scores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: interview_user
--

ALTER SEQUENCE public.qa_scores_id_seq OWNED BY public.qa_scores.id;


--
-- Name: question_criteria; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.question_criteria (
    question_id character varying(50) NOT NULL,
    criterion_id character varying(50) NOT NULL,
    weight numeric(3,2) DEFAULT 1.0,
    must_have boolean DEFAULT false,
    min_score numeric(3,2) DEFAULT 0.0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.question_criteria OWNER TO interview_user;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.questions (
    id character varying(50) NOT NULL,
    text text NOT NULL,
    type character varying(50) DEFAULT 'text'::character varying,
    max_duration_s integer DEFAULT 60,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    is_vacancy_specific boolean,
    category character varying(100),
    difficulty_level character varying(50)
);


ALTER TABLE public.questions OWNER TO interview_user;

--
-- Name: resume_blocks; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.resume_blocks (
    id character varying(50) NOT NULL,
    resume_id character varying(50) NOT NULL,
    block_type character varying(100) NOT NULL,
    block_name character varying(255) NOT NULL,
    extracted_text text,
    relevance_score numeric(5,2),
    confidence_score numeric(5,2),
    matched_requirements character varying[],
    missing_requirements character varying[],
    analysis_notes text,
    created_at timestamp with time zone DEFAULT now(),
    extracted_keywords character varying[]
);


ALTER TABLE public.resume_blocks OWNER TO interview_user;

--
-- Name: resume_skills; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.resume_skills (
    id character varying(50) NOT NULL,
    resume_id character varying(50) NOT NULL,
    skill_name character varying(255) NOT NULL,
    skill_category character varying(100),
    experience_level character varying(50),
    years_experience integer,
    confidence_score numeric(5,2),
    extracted_from text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.resume_skills OWNER TO interview_user;

--
-- Name: resumes; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.resumes (
    id character varying(50) NOT NULL,
    vacancy_id character varying(50),
    vacancy_code character varying(100),
    filename character varying(255) NOT NULL,
    original_filename character varying(255) NOT NULL,
    file_size integer NOT NULL,
    file_type character varying(50) NOT NULL,
    upload_date timestamp with time zone DEFAULT now(),
    status character varying(50),
    total_score numeric(5,2),
    confidence_score numeric(5,2),
    processing_errors text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.resumes OWNER TO interview_user;

--
-- Name: scenario_criteria_mappings; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.scenario_criteria_mappings (
    id character varying(50) NOT NULL,
    scenario_id character varying(50),
    criterion_id character varying(50),
    weight double precision DEFAULT 1.0 NOT NULL,
    is_mandatory boolean DEFAULT false,
    min_score double precision,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.scenario_criteria_mappings OWNER TO interview_user;

--
-- Name: scenario_nodes; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.scenario_nodes (
    id character varying(50) NOT NULL,
    scenario_id character varying(50) NOT NULL,
    question_id character varying(50),
    node_type character varying(50) NOT NULL,
    position_x integer,
    position_y integer,
    node_config json,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.scenario_nodes OWNER TO interview_user;

--
-- Name: scenario_transitions; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.scenario_transitions (
    id character varying(50) NOT NULL,
    scenario_id character varying(50) NOT NULL,
    from_node_id character varying(50) NOT NULL,
    to_node_id character varying(50) NOT NULL,
    condition_type character varying(50),
    condition_value json,
    priority integer,
    transition_label character varying(255),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.scenario_transitions OWNER TO interview_user;

--
-- Name: session_context; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.session_context (
    id character varying(50) NOT NULL,
    session_id character varying(50) NOT NULL,
    skill_assessments json,
    negative_responses json,
    current_path json,
    context_data json,
    current_node_id character varying(50),
    scenario_id character varying(50),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    contextual_questions jsonb
);


ALTER TABLE public.session_context OWNER TO interview_user;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.sessions (
    id character varying(50) NOT NULL,
    candidate_id integer,
    vacancy_id character varying(50),
    status character varying(50) DEFAULT 'created'::character varying,
    started_at timestamp with time zone,
    finished_at timestamp with time zone,
    total_score numeric(3,2),
    current_step integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    phone character varying(20),
    email character varying(100),
    total_steps integer DEFAULT 0,
    pass_rate numeric(3,2),
    vacancy_code character varying(50)
);


ALTER TABLE public.sessions OWNER TO interview_user;

--
-- Name: vacancies; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.vacancies (
    id character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    vacancy_code character varying(50),
    status character varying(50) DEFAULT 'active'::character varying,
    region character varying(100),
    city character varying(100),
    address text,
    employment_type character varying(50),
    contract_type character varying(50),
    work_schedule text,
    business_trips boolean DEFAULT false,
    salary_min numeric(10,2),
    salary_max numeric(10,2),
    total_income numeric(10,2),
    annual_bonus_percent numeric(5,2),
    bonus_description text,
    responsibilities text,
    requirements text,
    education_level character varying(100),
    experience_required character varying(100),
    special_programs text,
    computer_skills text,
    foreign_languages text,
    language_level character varying(50),
    additional_info text
);


ALTER TABLE public.vacancies OWNER TO interview_user;

--
-- Name: vacancy_questions; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.vacancy_questions (
    vacancy_id character varying(50) NOT NULL,
    question_id character varying(50) NOT NULL,
    step_no integer NOT NULL,
    question_weight numeric(3,2) DEFAULT 1.0,
    must_have boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.vacancy_questions OWNER TO interview_user;

--
-- Name: vacancy_section_keywords; Type: TABLE; Schema: public; Owner: interview_user
--

CREATE TABLE public.vacancy_section_keywords (
    id character varying(50) NOT NULL,
    vacancy_id character varying(50) NOT NULL,
    section_type public.sectiontype NOT NULL,
    keywords json NOT NULL,
    confidence_score double precision NOT NULL,
    extraction_date timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.vacancy_section_keywords OWNER TO interview_user;

--
-- Name: candidates id; Type: DEFAULT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.candidates ALTER COLUMN id SET DEFAULT nextval('public.candidates_id_seq'::regclass);


--
-- Name: media id; Type: DEFAULT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.media ALTER COLUMN id SET DEFAULT nextval('public.media_id_seq'::regclass);


--
-- Name: qa id; Type: DEFAULT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa ALTER COLUMN id SET DEFAULT nextval('public.qa_id_seq'::regclass);


--
-- Name: qa_scores id; Type: DEFAULT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa_scores ALTER COLUMN id SET DEFAULT nextval('public.qa_scores_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.alembic_version (version_num) FROM stdin;
e91aa8ea8925
\.


--
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.candidates (id, fio, phone, email, created_at, updated_at) FROM stdin;
1	Иванов Иван Иванович	+7-999-123-45-67	ivanov@example.com	2025-08-27 16:41:06.403192+00	2025-08-27 16:41:06.403192+00
2	Петрова Анна Сергеевна	+7-999-234-56-78	petrova@example.com	2025-08-27 16:41:06.403192+00	2025-08-27 16:41:06.403192+00
3	Сидоров Алексей Петрович	+7-999-345-67-89	sidorov@example.com	2025-08-27 16:41:06.403192+00	2025-08-27 16:41:06.403192+00
4	Иванов Иван Иванович	+7-999-123-45-67	ivanov@example.com	2025-08-30 14:53:56.599684+00	2025-08-30 14:53:56.599684+00
5	Петрова Анна Сергеевна	+7-999-234-56-78	petrova@example.com	2025-08-30 14:53:56.599684+00	2025-08-30 14:53:56.599684+00
6	Сидоров Алексей Петрович	+7-999-345-67-89	sidorov@example.com	2025-08-30 14:53:56.599684+00	2025-08-30 14:53:56.599684+00
\.


--
-- Data for Name: contextual_questions; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.contextual_questions (id, session_id, scenario_node_id, question_text, question_type, context_source, generated_at, is_used, used_at, created_at, updated_at) FROM stdin;
CONTEXT_Q_8B05AAE9	1618ced8-05b7-49b3-904d-c3ce08b58533	SCENARIO_917B6C27_node_1	Какие инструменты и подходы вы используете для документирования бизнес-требований, чтобы обеспечить их однозначность и минимизировать риск недоразумений между бизнесом и технической командой? Приведите пример сложного кейса, с которым вы сталкивались.	technical	{"source": "Кандидату требуется экспертное владение навыком подготовки бизнес-требований и intermediate уровень в разработке технической документации. Вопрос направлен на проверку подходов к устранению типичных проблем в коммуникации между командами."}	2025-08-31 18:27:53.42633+00	t	2025-08-31 18:34:40.360942+00	2025-08-31 18:27:53.42633+00	2025-08-31 18:34:40.360095+00
CONTEXT_Q_B371856E	bf89bae1-9ff1-47d7-bf85-ccca6b0beb3e	SCENARIO_917B6C27_node_1	Какие ключевые аспекты вы учитываете при подготовке бизнес-требований для оптимизации мониторинга мошеннических операций? Приведите пример из вашего опыта.	technical	{"source": "Вопрос фокусируется на требуемых навыках подготовки бизнес-требований (expert уровень), понимания мошеннических операций и оптимизации антифрод-мониторинга (intermediate уровень). Это позволяет проверить техническую глубину знаний кандидата в контексте анализа и борьбы с мошенничеством."}	2025-08-31 18:37:20.870569+00	t	2025-08-31 18:37:46.214531+00	2025-08-31 18:37:20.870569+00	2025-08-31 18:37:46.213683+00
\.


--
-- Data for Name: criteria; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.criteria (id, code, name, description, created_at, updated_at) FROM stdin;
FASTAPI	FASTAPI	Опыт с FastAPI	Знание и опыт использования FastAPI фреймворка	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
ASYNCIO	ASYNCIO	Асинхронное программирование	Понимание и опыт работы с asyncio	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
DATABASE	DATABASE	Работа с БД	Опыт работы с различными базами данных	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
TESTING	TESTING	Тестирование	Подход к тестированию кода	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
MICROSERVICES	MICROSERVICES	Микросервисы	Опыт работы с микросервисной архитектурой	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
DEPLOYMENT	DEPLOYMENT	Деплой	Опыт деплоя приложений	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
PROBLEM_SOLVING	PROBLEM_SOLVING	Решение проблем	Способность решать сложные технические задачи	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
TEAMWORK	TEAMWORK	Командная работа	Опыт работы в команде	2025-08-27 16:41:06.407426+00	2025-08-27 16:41:06.407426+00
\.


--
-- Data for Name: dynamic_criteria; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.dynamic_criteria (id, vacancy_id, skill_name, category, importance, required_level, is_mandatory, description, alternatives, created_at, updated_at) FROM stdin;
DC_051833A4	SWE_BACK_001	знание серверного оборудования х86	other	1	beginner	t	Базовые знания об устройстве и принципах работы серверного оборудования х86	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u044b\\u043c \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435\\u043c"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_1B573816	SWE_BACK_001	знание структурированных кабельных систем	other	0.8	beginner	t	Базовые знания о медных и оптических структурированных кабельных системах	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u043c\\u0438 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430\\u043c\\u0438"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_F72F33A2	SWE_BACK_001	знание сетей передачи и хранения данных	other	0.8	beginner	t	Базовые знания о сетях передачи и хранения данных (LAN и SAN)	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 LAN \\u0438 SAN"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_30395874	SWE_BACK_001	знание центров обработки данных	other	0.7	beginner	t	Базовые знания о принципах работы центров обработки данных	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0426\\u041e\\u0414"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_5321F05A	SWE_BACK_001	первичная диагностика серверного оборудования х86	other	1	beginner	t	Навык первичной диагностики серверного оборудования х86	["\\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_FCF31438	SWE_BACK_001	работа с Excel	tools	0.8	intermediate	t	Уверенные навыки работы с Excel для ведения данных и отчетов	["Microsoft Excel"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_64965B36	SWE_BACK_001	работа с Word	tools	0.7	intermediate	t	Уверенные навыки работы с Word для подготовки документации	["Microsoft Word"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_8923BCE6	SWE_BACK_001	работа с Visio	tools	0.6	intermediate	t	Уверенные навыки работы с Visio для создания схем и диаграмм	["Microsoft Visio"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_46F7A970	SWE_BACK_001	грамотная устная и письменная речь	soft_skills	0.9	expert	t	Грамотная устная и письменная речь для общения и ведения документации	["\\u043a\\u043e\\u043c\\u043c\\u0443\\u043d\\u0438\\u043a\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0435 \\u043d\\u0430\\u0432\\u044b\\u043a\\u0438"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_B062FA74	SWE_BACK_001	ответственность	soft_skills	0.8	expert	t	Ответственность за выполнение задач и соблюдение сроков	["\\u043d\\u0430\\u0434\\u0435\\u0436\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_6EEDB5D4	SWE_BACK_001	аккуратность в работе	soft_skills	0.7	expert	t	Аккуратность при выполнении задач, особенно связанных с оборудованием	["\\u0432\\u043d\\u0438\\u043c\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_7160BAAA	SWE_BACK_001	исполнительность	soft_skills	0.8	expert	t	Исполнительность в выполнении поставленных задач	["\\u0434\\u0438\\u0441\\u0446\\u0438\\u043f\\u043b\\u0438\\u043d\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_3F439185	SWE_BACK_001	инициативность	soft_skills	0.6	expert	f	Инициативность в предложении улучшений и решений	["\\u043f\\u0440\\u043e\\u0430\\u043a\\u0442\\u0438\\u0432\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 00:39:24.798455+00	2025-08-31 00:39:24.798455+00
DC_7A9A7F4B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_D37CAD6F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_188FE711	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_37BE55CF	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_864B9CD6	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_98D845FB	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_F28206F7	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_2F42B412	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_45ADAD48	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_6AB5D121	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_58394515	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_B85B34C6	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_6F88DABF	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_7AAAA70D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_8A32BC70	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_10D036B0	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_BA45D403	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_4E9624A3	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 00:56:53.365337+00	2025-08-31 00:56:53.365337+00
DC_56F40868	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_0578995A	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_EF568181	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_A6ECEB80	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_8509E16F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_7D0016B2	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_F5C6A2B0	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_16C8A347	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_6BAB6C6E	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_03437823	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_2FEA11F8	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_5004F7AD	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_5BF67D0C	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_2DED91D5	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_D8518A47	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_A37EFE38	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_3E9187A3	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_AEE5F99F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_A2C7E094	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 00:59:23.315612+00	2025-08-31 00:59:23.315612+00
DC_7AF5A047	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_59AD7734	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_A47881DF	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_14EB222D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_3912820E	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_8B1FD041	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_6222905D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_3B41FFE7	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_4B86CC0D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_FC34D7EB	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_A17D018C	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_EEBD483D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_C06CD6F7	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_F4EEDE0B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_4ACFDF61	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_FD7DA201	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_2F56CA8B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_3D5009F2	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 01:00:25.873698+00	2025-08-31 01:00:25.873698+00
DC_57DBEAC8	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_3D792414	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_FB0C6A3B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_5CD9E100	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_8E41AA05	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_6D022644	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_6047C57D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_EFAE39F1	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_0FF6490F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_99790CDC	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_E77BAFDA	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_6986DF25	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_1843C27F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_E150BA6B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_3A75C79B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_CDA6A88B	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_490E37EF	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 01:01:35.245721+00	2025-08-31 01:01:35.245721+00
DC_E9D94E13	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_8AD420A5	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_826E38CB	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_74F1AE4F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_27AA9298	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_C1D5EA16	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_2B3741B2	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_D82672A3	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_89160AAC	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_4D450128	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_4EA3AD83	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_329C4AC9	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_7DF29AE4	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_13F9081A	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_B55B8B41	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_A886DA18	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_FDA18F32	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_9AE62C8D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 01:02:56.106011+00	2025-08-31 01:02:56.106011+00
DC_FB042B8A	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_4BFEEDA7	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_7A5C3E4F	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_CE68EF45	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_C052EC21	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_CB9E7CD7	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_8D4252B7	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_67980DFD	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_A9D73CEA	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_A8E65A22	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_6D876D08	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_A56DB3CA	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_66B82996	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_B142F68D	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_5EE15513	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_52B1C668	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_3BB9E9DC	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_F8D29743	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 01:04:33.277006+00	2025-08-31 01:04:33.277006+00
DC_7B0D9BC9	SWE_BACK_001	знание серверного оборудования х86	other	1	beginner	t	Базовые знания об устройстве и принципах работы серверного оборудования х86	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u044b\\u043c \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435\\u043c"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_C6ACDC8D	SWE_BACK_001	знание структурированных кабельных систем	other	0.8	beginner	t	Базовые знания о медных и оптических структурированных кабельных системах	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u043c\\u0438 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430\\u043c\\u0438"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_53B61ADA	SWE_BACK_001	знание сетей передачи и хранения данных	other	0.8	beginner	t	Базовые знания о сетях передачи и хранения данных (LAN и SAN)	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 LAN \\u0438 SAN"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_40B0E7E1	SWE_BACK_001	знание центров обработки данных	other	0.7	beginner	t	Базовые знания о принципах работы центров обработки данных	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0426\\u041e\\u0414"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_5BE184E6	SWE_BACK_001	первичная диагностика серверного оборудования х86	other	1	beginner	t	Навык первичной диагностики серверного оборудования х86	["\\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_AF65A949	SWE_BACK_001	работа с Excel	tools	0.8	intermediate	t	Уверенные навыки работы с Excel для ведения данных и отчетов	["Microsoft Excel"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_9AFB62B4	SWE_BACK_001	работа с Word	tools	0.7	intermediate	t	Уверенные навыки работы с Word для подготовки документации	["Microsoft Word"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_138CC52B	SWE_BACK_001	работа с Visio	tools	0.6	intermediate	t	Уверенные навыки работы с Visio для создания схем и диаграмм	["Microsoft Visio"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_0F498550	SWE_BACK_001	грамотная устная и письменная речь	soft_skills	0.9	expert	t	Грамотная устная и письменная речь для общения и ведения документации	["\\u043a\\u043e\\u043c\\u043c\\u0443\\u043d\\u0438\\u043a\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0435 \\u043d\\u0430\\u0432\\u044b\\u043a\\u0438"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_7959D560	SWE_BACK_001	ответственность	soft_skills	0.8	expert	t	Ответственность за выполнение задач и соблюдение сроков	["\\u043d\\u0430\\u0434\\u0435\\u0436\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_6DA2AF36	SWE_BACK_001	аккуратность в работе	soft_skills	0.7	expert	t	Аккуратность при выполнении задач, особенно связанных с оборудованием	["\\u0432\\u043d\\u0438\\u043c\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_83376A51	SWE_BACK_001	исполнительность	soft_skills	0.8	expert	t	Исполнительность в выполнении поставленных задач	["\\u0434\\u0438\\u0441\\u0446\\u0438\\u043f\\u043b\\u0438\\u043d\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_A5720EFA	SWE_BACK_001	инициативность	soft_skills	0.6	expert	f	Инициативность в предложении улучшений и решений	["\\u043f\\u0440\\u043e\\u0430\\u043a\\u0442\\u0438\\u0432\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:18:51.916813+00	2025-08-31 01:18:51.916813+00
DC_DB56D0AB	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Word	tools	0.8	intermediate	t	Уверенное владение текстовым редактором для подготовки документации.	["Word Processor"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_0973BF55	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft Excel	tools	0.9	intermediate	t	Уверенное владение табличным процессором для анализа данных и отчетности.	["Spreadsheet Software"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_A6AD93D4	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Microsoft PowerPoint	tools	0.7	intermediate	t	Уверенное владение инструментом для создания презентаций.	["Presentation Software"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_596432B8	SWE_BACK_001	работа с Visio	tools	0.6	intermediate	t	Уверенные навыки работы с Visio для создания схем и диаграмм	["Microsoft Visio"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_9D0B8A87	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Подготовка бизнес-требований	analytics	1	expert	t	Навыки подготовки бизнес-требований для разработки и развития систем.	["Business Requirements Documentation"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_6F1E51EA	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с антифрод-системами	other	0.7	intermediate	f	Опыт работы с программным обеспечением для противодействия мошенничеству.	["Fraud Prevention Systems"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_A41F5845	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с корпоративными картами	other	0.6	intermediate	f	Опыт работы с операциями по корпоративным картам.	["Corporate Card Operations"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_CC26229E	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание плана счетов клиентов ЮЛ	analytics	0.6	intermediate	f	Знание структуры и логики плана счетов для юридических лиц.	["Corporate Client Account Plan"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_681C78D4	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание клиентского пути ЮЛ в банке	analytics	0.7	intermediate	f	Представление о процессе взаимодействия юридических лиц с банком.	["Corporate Client Journey"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_A6DD40EB	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Опыт работы с фронтальными системами ДБО	other	0.7	intermediate	f	Опыт работы с системами дистанционного банковского обслуживания.	["Front-End Banking Systems"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_8BF11FAB	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание мошеннических сценариев	analytics	0.8	intermediate	f	Понимание сценариев мошенничества и методов их предотвращения.	["Fraud Scenarios Analysis"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_2CA01E81	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка технической документации	analytics	0.9	expert	f	Навыки разработки технической документации, включая ТЗ, методики и руководства.	["Technical Documentation Writing"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_DFCDD355	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Понимание принципов работы с СУБД	database	0.8	intermediate	f	Понимание принципов работы с системами управления базами данных.	["Database Management Systems"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_AE329247	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание технологий разработки ПО	programming	0.7	intermediate	f	Знание основных технологий и протоколов, применяемых при разработке программного обеспечения.	["Software Development Technologies"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_35FF0EB2	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Знание правил платёжных систем	analytics	0.8	intermediate	f	Знание правил работы платёжных систем и логики проведения транзакций.	["Payment Systems Rules"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_8C51167A	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Управление системой противодействия мошенничеству	management	1	expert	t	Управление системой противодействия мошенничеству и инструментами управления рисками.	["Fraud Management Systems"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_091F3023	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Формирование предложений по оптимизации	analytics	0.9	expert	t	Формирование предложений по оптимизации и улучшению правил антифрод-мониторинга.	["Optimization Proposals"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_5DCCD33E	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Анализ и формирование требований	analytics	1	expert	t	Анализ и формирование функциональных и бизнес-требований для разработки.	["Requirements Analysis"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_CA6A94CA	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Разработка тест-кейсов	testing	0.8	intermediate	t	Участие в разработке тест-кейсов и функциональном тестировании.	["Test Case Design"]	2025-08-31 01:20:49.469629+00	2025-08-31 01:20:49.469629+00
DC_FAAED486	SWE_BACK_001	знание серверного оборудования х86	other	1	beginner	t	Базовые знания об устройстве и принципах работы серверного оборудования х86	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u044b\\u043c \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435\\u043c"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_95157690	SWE_BACK_001	знание структурированных кабельных систем	other	0.8	beginner	t	Базовые знания о медных и оптических структурированных кабельных системах	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u043c\\u0438 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430\\u043c\\u0438"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_5AD50C48	SWE_BACK_001	знание сетей передачи и хранения данных	other	0.8	beginner	t	Базовые знания о сетях передачи и хранения данных (LAN и SAN)	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 LAN \\u0438 SAN"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_6C455EE2	SWE_BACK_001	знание центров обработки данных	other	0.7	beginner	t	Базовые знания о принципах работы центров обработки данных	["\\u043e\\u0441\\u043d\\u043e\\u0432\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0426\\u041e\\u0414"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_BB650A26	SWE_BACK_001	первичная диагностика серверного оборудования х86	other	1	beginner	t	Навык первичной диагностики серверного оборудования х86	["\\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_C9C63AE0	SWE_BACK_001	работа с Excel	tools	0.8	intermediate	t	Уверенные навыки работы с Excel для ведения данных и отчетов	["Microsoft Excel"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_F5029AE1	SWE_BACK_001	работа с Word	tools	0.7	intermediate	t	Уверенные навыки работы с Word для подготовки документации	["Microsoft Word"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_2E87BCAC	SWE_BACK_001	грамотная устная и письменная речь	soft_skills	0.9	expert	t	Грамотная устная и письменная речь для общения и ведения документации	["\\u043a\\u043e\\u043c\\u043c\\u0443\\u043d\\u0438\\u043a\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0435 \\u043d\\u0430\\u0432\\u044b\\u043a\\u0438"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_8EB3A78F	SWE_BACK_001	ответственность	soft_skills	0.8	expert	t	Ответственность за выполнение задач и соблюдение сроков	["\\u043d\\u0430\\u0434\\u0435\\u0436\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_933233B6	SWE_BACK_001	аккуратность в работе	soft_skills	0.7	expert	t	Аккуратность при выполнении задач, особенно связанных с оборудованием	["\\u0432\\u043d\\u0438\\u043c\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_BC89B741	SWE_BACK_001	исполнительность	soft_skills	0.8	expert	t	Исполнительность в выполнении поставленных задач	["\\u0434\\u0438\\u0441\\u0446\\u0438\\u043f\\u043b\\u0438\\u043d\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
DC_ABE7ED7B	SWE_BACK_001	инициативность	soft_skills	0.6	expert	f	Инициативность в предложении улучшений и решений	["\\u043f\\u0440\\u043e\\u0430\\u043a\\u0442\\u0438\\u0432\\u043d\\u043e\\u0441\\u0442\\u044c"]	2025-08-31 01:21:20.13111+00	2025-08-31 01:21:20.13111+00
\.


--
-- Data for Name: interview_codes; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.interview_codes (id, code, resume_id, is_used, created_at, used_at) FROM stdin;
CODE_1E5E7F42	812939	RESUME_54929C26	f	2025-08-31 00:05:56.580137+00	\N
CODE_D5D787CE	659778	RESUME_54929C26	t	2025-08-31 00:06:21.378563+00	2025-08-31 00:07:06.780885+00
CODE_630E6868	562376	RESUME_54929C26	t	2025-09-01 00:12:19.075999+00	2025-09-01 00:12:29.713091+00
CODE_263DCD2B	329185	RESUME_54929C26	t	2025-09-01 00:16:30.364166+00	2025-09-01 00:16:43.158492+00
CODE_A986A2ED	331301	RESUME_54929C26	t	2025-09-01 00:19:04.960187+00	2025-09-01 00:19:17.931918+00
CODE_A5C83CEA	990439	RESUME_54929C26	t	2025-09-01 00:27:22.098495+00	2025-09-01 00:27:30.161699+00
CODE_016D6B72	476169	RESUME_54929C26	t	2025-09-01 00:30:56.514611+00	2025-09-01 00:31:05.441785+00
CODE_F776E00F	257232	RESUME_54929C26	t	2025-09-01 00:34:05.914964+00	2025-09-01 00:34:17.133095+00
CODE_B76FB19B	279223	RESUME_54929C26	t	2025-09-01 00:48:52.232326+00	2025-09-01 00:48:59.913673+00
CODE_58630BC8	827587	RESUME_54929C26	t	2025-09-01 01:07:38.94722+00	2025-09-01 01:07:48.470801+00
CODE_ED5D3E22	488832	RESUME_54929C26	t	2025-09-01 01:18:01.040622+00	2025-09-01 01:18:07.046087+00
CODE_5B3232B3	054933	RESUME_54929C26	t	2025-09-01 01:29:26.935473+00	2025-09-01 01:29:34.88433+00
CODE_8A4194B3	200212	RESUME_54929C26	t	2025-09-01 01:39:19.649813+00	2025-09-01 01:39:27.168296+00
CODE_46DD741C	676378	RESUME_54929C26	t	2025-09-01 01:46:32.283083+00	2025-09-01 01:46:39.488533+00
CODE_4129F006	720063	RESUME_54929C26	t	2025-09-01 01:55:36.756359+00	2025-09-01 01:55:44.958708+00
CODE_9FA32AA8	885446	RESUME_54929C26	t	2025-09-01 01:58:59.058077+00	2025-09-01 01:59:04.498412+00
CODE_7ADD7916	912503	RESUME_54929C26	t	2025-09-01 02:13:15.482835+00	2025-09-01 02:13:21.418523+00
CODE_042C32C4	779203	RESUME_54929C26	t	2025-09-01 02:19:18.260941+00	2025-09-01 02:19:27.411184+00
CODE_CC6FE093	417939	RESUME_54929C26	t	2025-09-01 02:28:16.012961+00	2025-09-01 02:28:20.837902+00
CODE_69AD5EA3	281572	RESUME_54929C26	t	2025-09-02 22:19:45.667024+00	2025-09-02 22:19:57.641819+00
CODE_A34F117B	467880	RESUME_54929C26	t	2025-09-02 22:33:36.190827+00	2025-09-02 22:33:43.571712+00
CODE_61832AEB	045802	RESUME_54929C26	t	2025-09-02 22:44:15.803011+00	2025-09-02 22:44:23.124641+00
CODE_1E865FF8	825939	RESUME_54929C26	t	2025-09-02 22:53:41.50149+00	2025-09-02 22:53:48.256545+00
CODE_26B4023C	142968	RESUME_54929C26	t	2025-09-02 23:15:41.975401+00	2025-09-02 23:15:49.755168+00
CODE_FF1FB2D5	321769	RESUME_54929C26	t	2025-09-02 23:29:28.24806+00	2025-09-02 23:29:36.478094+00
CODE_C930D08F	984704	RESUME_54929C26	t	2025-09-02 23:52:57.480333+00	2025-09-02 23:53:05.050889+00
CODE_A7FAB0FB	884779	RESUME_54929C26	t	2025-09-03 00:02:04.305098+00	2025-09-03 00:02:09.915544+00
CODE_9F53D266	724904	RESUME_54929C26	t	2025-09-03 00:17:59.132517+00	2025-09-03 00:18:05.358978+00
CODE_A1B36400	012901	RESUME_54929C26	t	2025-09-03 00:22:21.943863+00	2025-09-03 00:22:27.910193+00
CODE_311BB834	504127	RESUME_54929C26	t	2025-09-03 00:41:06.6828+00	2025-09-03 00:41:15.754638+00
CODE_27F1245B	300602	RESUME_54929C26	t	2025-09-03 10:51:55.129776+00	2025-09-03 10:52:04.343449+00
CODE_91C7881D	349086	RESUME_54929C26	f	2025-09-03 18:47:49.956154+00	\N
CODE_38DC5499	794518	RESUME_4213C3EF	t	2025-09-03 18:49:25.252212+00	2025-09-03 18:51:32.88892+00
CODE_DC3FC8FF	631321	RESUME_54929C26	t	2025-09-03 18:53:42.781471+00	2025-09-03 18:53:53.626296+00
CODE_8D4F0DC8	815872	RESUME_4213C3EF	f	2025-09-07 19:39:33.999823+00	\N
CODE_EFF289A9	813488	RESUME_54929C26	t	2025-09-07 19:39:50.784798+00	2025-09-07 19:39:58.818442+00
CODE_994026DD	122603	RESUME_4213C3EF	f	2025-09-07 21:21:15.269365+00	\N
CODE_1E7AD9D8	605808	RESUME_54929C26	t	2025-09-07 22:33:45.859369+00	2025-09-07 22:33:52.691947+00
CODE_3A788066	320429	RESUME_54929C26	f	2025-09-08 16:03:51.110409+00	\N
CODE_EED23CD5	784992	RESUME_4213C3EF	t	2025-09-08 16:04:33.562048+00	2025-09-08 16:04:45.299682+00
\.


--
-- Data for Name: interview_scenarios; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.interview_scenarios (id, vacancy_id, name, description, is_active, version, created_at, updated_at) FROM stdin;
SCENARIO_844827A6	SWE_BACK_001	Тестовый сценарий	Автоматически сгенерированный сценарий	t	1.0	2025-08-31 00:39:33.818866+00	2025-08-31 00:39:33.818866+00
SCENARIO_A9DB7161	af625a8d-1f69-4aea-9d2f-2d5b504ef215	Автоматический сценарий для БА	Адаптивный сценарий интервью для оценки навыков и опыта кандидата на позицию Business Analyst.	t	1.0	2025-08-31 01:04:33.317278+00	2025-08-31 01:04:33.317278+00
SCENARIO_A0EE5ADE	SWE_BACK_001	Smart Backend Developer Interview	Адаптивный сценарий для интервью Backend Developer с умной навигацией	t	1.0	2025-08-31 01:21:20.143038+00	2025-08-31 01:21:20.143038+00
\.


--
-- Data for Name: media; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.media (id, session_id, kind, url, duration_ms, file_size_bytes, created_at) FROM stdin;
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.messages (id, session_id, text, message_type, audio_url, transcription_confidence, "timestamp", created_at, tone_analysis) FROM stdin;
msg-1756576349669-am0f3oe4f	153c687f-a592-47dc-a577-3dc60170d9ff	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-08-30 17:52:29.669+00	2025-08-30 17:52:29.674435+00	\N
msg-1756576349710-iduthiotx	153c687f-a592-47dc-a577-3dc60170d9ff	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	avatar	\N	\N	2025-08-30 17:52:29.711+00	2025-08-30 17:52:29.716301+00	\N
msg-1756588900664-m882xe4ft	fe47e667-ea4f-4d83-abc9-58a81295a685	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-08-30 21:21:40.664+00	2025-08-30 21:21:40.676575+00	\N
msg-1756588900722-yrnk0az39	fe47e667-ea4f-4d83-abc9-58a81295a685	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	avatar	\N	\N	2025-08-30 21:21:40.722+00	2025-08-30 21:21:40.727874+00	\N
msg-1756588918739-1ujdas3c4	fe47e667-ea4f-4d83-abc9-58a81295a685	А почему ты сразу спрашиваешь про фастапию? Я реклевал много проектах на этом фуилбурге.	user	minio://audio-files/fe47e667-ea4f-4d83-abc9-58a81295a685_recording_1756588918739.webm	-1	2025-08-30 21:22:05.217+00	2025-08-30 21:22:05.224347+00	\N
msg-1756588930474-nttv8begn	fe47e667-ea4f-4d83-abc9-58a81295a685	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	avatar	\N	\N	2025-08-30 21:22:10.474+00	2025-08-30 21:22:10.479858+00	\N
msg-1756598832359-hj7j2jj3l	ad597e46-2ba9-4482-bda9-b2253d60ecab	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-08-31 00:07:12.359+00	2025-08-31 00:07:12.369084+00	\N
msg-1756598837474-x5kixoomd	ad597e46-2ba9-4482-bda9-b2253d60ecab	Дай готов!	user	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598837474.webm	-1	2025-08-31 00:07:18.672+00	2025-08-31 00:07:18.676356+00	\N
msg-1756598849785-ne2bo3e67	ad597e46-2ba9-4482-bda9-b2253d60ecab	Я вилния скройку крупных паций.	user	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598849785.webm	-1	2025-08-31 00:07:31.29+00	2025-08-31 00:07:31.29402+00	\N
msg-1756598863322-9vr90uon3	ad597e46-2ba9-4482-bda9-b2253d60ecab	это крупные проекты.	user	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598863322.webm	0	2025-08-31 00:07:47.104+00	2025-08-31 00:07:47.108444+00	\N
msg-1756598880467-sdvdtbqdz	ad597e46-2ba9-4482-bda9-b2253d60ecab	анализировал требования и составлял документы.	user	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598880467.webm	0	2025-08-31 00:08:07.077+00	2025-08-31 00:08:07.081628+00	\N
msg-1756598964809-nqlrh5xnd	ad597e46-2ba9-4482-bda9-b2253d60ecab	Спасибо за участие в интервью. Ваши ответы записаны и будут оценены. Удачи!	avatar	\N	\N	2025-08-31 00:09:24.809+00	2025-08-31 00:09:24.815606+00	\N
msg-1756685962122-xqw1tgxlx	f26a8d59-b340-4a31-b07f-650f89818097	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 00:19:22.123+00	2025-09-01 00:19:22.129952+00	\N
msg-1756685962211-mb4a4wvv1	f26a8d59-b340-4a31-b07f-650f89818097	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:19:22.211+00	2025-09-01 00:19:22.216156+00	\N
msg-1756685977801-mnoeyhqj9	f26a8d59-b340-4a31-b07f-650f89818097	А я не знаю, какая бы кончая какие технологии.	user	minio://audio-files/f26a8d59-b340-4a31-b07f-650f89818097_recording_1756685977801.webm	0	2025-09-01 00:19:42.961+00	2025-09-01 00:19:42.967425+00	\N
msg-1756685989098-liiwlxhok	f26a8d59-b340-4a31-b07f-650f89818097	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:19:49.098+00	2025-09-01 00:19:49.106056+00	\N
msg-1756686452137-gnkikyjay	dd299d81-63b2-42f5-a10f-8af6bb8176d7	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 00:27:32.138+00	2025-09-01 00:27:32.145644+00	\N
msg-1756686452212-0cj1b6vrj	dd299d81-63b2-42f5-a10f-8af6bb8176d7	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:27:32.212+00	2025-09-01 00:27:32.217816+00	\N
msg-1756686459129-vbfvpl4zh	dd299d81-63b2-42f5-a10f-8af6bb8176d7	Привет!	user	minio://audio-files/dd299d81-63b2-42f5-a10f-8af6bb8176d7_recording_1756686459129.webm	-1	2025-09-01 00:27:43.269+00	2025-09-01 00:27:43.274203+00	\N
msg-1756686469052-2nshvbmzg	dd299d81-63b2-42f5-a10f-8af6bb8176d7	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:27:49.052+00	2025-09-01 00:27:49.060104+00	\N
msg-1756686682229-yyrb7jd6b	87240571-1983-4a50-83a9-f7859a04ab30	СПОКОЙНАЯ МУЗЫКА Привет!	user	minio://audio-files/87240571-1983-4a50-83a9-f7859a04ab30_recording_1756686682229.webm	-1	2025-09-01 00:31:25.659+00	2025-09-01 00:31:25.664479+00	\N
msg-1756572864821-hizui15ne	c55aab56-a42f-45a7-afd8-59f4b81383b7	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-08-30 16:54:24.822+00	2025-08-30 16:54:24.826836+00	\N
msg-1756572864852-hgcqy5lqk	c55aab56-a42f-45a7-afd8-59f4b81383b7	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	avatar	\N	\N	2025-08-30 16:54:24.852+00	2025-08-30 16:54:24.856819+00	\N
msg-1756572872202-tuszcdf32	c55aab56-a42f-45a7-afd8-59f4b81383b7	Could not transcribe audio	user	minio://audio-files/c55aab56-a42f-45a7-afd8-59f4b81383b7_recording_1756572872202.webm	0	2025-08-30 16:54:42.948+00	2025-08-30 16:54:42.952095+00	\N
msg-1756572886274-9hq4fccx3	c55aab56-a42f-45a7-afd8-59f4b81383b7	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	avatar	\N	\N	2025-08-30 16:54:46.274+00	2025-08-30 16:54:46.278369+00	\N
msg-1756572932213-llm798dqy	c55aab56-a42f-45a7-afd8-59f4b81383b7	Спасибо за участие в интервью. Ваши ответы записаны и будут оценены. Удачи!	avatar	\N	\N	2025-08-30 16:55:32.213+00	2025-08-30 16:55:32.217426+00	\N
msg-1756686676229-canulsz0w	87240571-1983-4a50-83a9-f7859a04ab30	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 00:31:16.23+00	2025-09-01 00:31:16.235314+00	\N
msg-1756686676293-f44iy3578	87240571-1983-4a50-83a9-f7859a04ab30	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:31:16.293+00	2025-09-01 00:31:16.297754+00	\N
msg-1756686712875-qrc9y0h2s	87240571-1983-4a50-83a9-f7859a04ab30	А я не помню, как это.	user	minio://audio-files/87240571-1983-4a50-83a9-f7859a04ab30_recording_1756686712875.webm	-1	2025-09-01 00:31:56.816+00	2025-09-01 00:31:56.821555+00	\N
msg-1756686691306-wjajd2leb	87240571-1983-4a50-83a9-f7859a04ab30	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:31:31.306+00	2025-09-01 00:31:31.311686+00	\N
msg-1756686733966-umlti7e5f	87240571-1983-4a50-83a9-f7859a04ab30	у меня в Excel.	user	minio://audio-files/87240571-1983-4a50-83a9-f7859a04ab30_recording_1756686733966.webm	-1	2025-09-01 00:32:16.466+00	2025-09-01 00:32:16.469372+00	\N
msg-1756686722484-hg90upxl2	87240571-1983-4a50-83a9-f7859a04ab30	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:32:02.484+00	2025-09-01 00:32:02.489403+00	\N
msg-1756686743270-cligx6s79	87240571-1983-4a50-83a9-f7859a04ab30	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:32:23.27+00	2025-09-01 00:32:23.284481+00	\N
msg-1756686860909-6z71zlyw7	85b86496-6fcd-4bbc-98d0-2f4c5dfb6504	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 00:34:20.909+00	2025-09-01 00:34:20.914431+00	\N
msg-1756686860949-hs3pnu1g1	85b86496-6fcd-4bbc-98d0-2f4c5dfb6504	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:34:20.949+00	2025-09-01 00:34:20.954784+00	\N
msg-1756686864269-l73by9myh	85b86496-6fcd-4bbc-98d0-2f4c5dfb6504	Раз, два, три, четыре, пять.	user	minio://audio-files/85b86496-6fcd-4bbc-98d0-2f4c5dfb6504_recording_1756686864269.webm	0	2025-09-01 00:34:25.597+00	2025-09-01 00:34:25.600897+00	\N
msg-1756686871260-rp00c2iq3	85b86496-6fcd-4bbc-98d0-2f4c5dfb6504	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:34:31.26+00	2025-09-01 00:34:31.264197+00	\N
msg-1756687741230-05qz7sfvk	2905ca67-8f89-4563-94d4-7f6d69efc095	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 00:49:01.23+00	2025-09-01 00:49:01.237103+00	\N
msg-1756687741305-e8ooff97p	2905ca67-8f89-4563-94d4-7f6d69efc095	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 00:49:01.305+00	2025-09-01 00:49:01.308974+00	\N
msg-1756688871868-mvt1t0wve	b7a7ee54-5ae5-45fc-8ad5-9f51ff109815	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:07:51.869+00	2025-09-01 01:07:51.875793+00	\N
msg-1756688871948-pbp2t7g9n	b7a7ee54-5ae5-45fc-8ad5-9f51ff109815	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:07:51.948+00	2025-09-01 01:07:51.953239+00	\N
msg-1756688887549-svmd0gu70	b7a7ee54-5ae5-45fc-8ad5-9f51ff109815	Привет! Ичё?	user	minio://audio-files/b7a7ee54-5ae5-45fc-8ad5-9f51ff109815_recording_1756688887550.webm	-1	2025-09-01 01:08:13.942+00	2025-09-01 01:08:13.948167+00	\N
msg-1756688907236-fgwa7s3po	b7a7ee54-5ae5-45fc-8ad5-9f51ff109815	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:08:27.236+00	2025-09-01 01:08:27.244309+00	\N
msg-1756689491252-p0kazdg1y	c5f1edfb-4f41-4be9-b3b9-25f3f96c2181	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:18:11.252+00	2025-09-01 01:18:11.260315+00	\N
msg-1756689491335-lyd9kis1q	c5f1edfb-4f41-4be9-b3b9-25f3f96c2181	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:18:11.335+00	2025-09-01 01:18:11.339619+00	\N
msg-1756689514835-ezqjny71s	c5f1edfb-4f41-4be9-b3b9-25f3f96c2181	Рас? 3 4 5	user	minio://audio-files/c5f1edfb-4f41-4be9-b3b9-25f3f96c2181_recording_1756689514835.webm	-1	2025-09-01 01:18:40.661+00	2025-09-01 01:18:40.665695+00	\N
msg-1756689534702-wh6htlr12	c5f1edfb-4f41-4be9-b3b9-25f3f96c2181	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:18:54.702+00	2025-09-01 01:18:54.710202+00	\N
msg-1756690178376-8afr6yf3s	f6265ee7-76f4-41f3-bec3-228982c39989	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:29:38.376+00	2025-09-01 01:29:38.382695+00	\N
msg-1756690178422-3cudxu0tj	f6265ee7-76f4-41f3-bec3-228982c39989	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:29:38.422+00	2025-09-01 01:29:38.427493+00	\N
msg-1756690196515-a6p0bnoof	f6265ee7-76f4-41f3-bec3-228982c39989	Привет, раз-два-три. 4,5,6,7,8,1,25 А.Синецкая	user	minio://audio-files/f6265ee7-76f4-41f3-bec3-228982c39989_recording_1756690196515.webm	0	2025-09-01 01:30:02.543+00	2025-09-01 01:30:02.546676+00	\N
msg-1756690216661-ek6lzslyy	f6265ee7-76f4-41f3-bec3-228982c39989	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:30:16.662+00	2025-09-01 01:30:16.668504+00	\N
msg-1756690768492-aomsph17s	09a2d860-1f50-4ef2-b672-758e4e5f2251	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:39:28.492+00	2025-09-01 01:39:28.497117+00	\N
msg-1756690768533-hpu4qt5iv	09a2d860-1f50-4ef2-b672-758e4e5f2251	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:39:28.533+00	2025-09-01 01:39:28.536688+00	\N
msg-1756690901472-myzmnf0o6	09a2d860-1f50-4ef2-b672-758e4e5f2251	Рас. Два. 3,4,5,6	user	minio://audio-files/09a2d860-1f50-4ef2-b672-758e4e5f2251_recording_1756690901472.webm	-1	2025-09-01 01:41:48.549+00	2025-09-01 01:41:48.553085+00	\N
msg-1756690926177-aicugct7n	09a2d860-1f50-4ef2-b672-758e4e5f2251	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:42:06.177+00	2025-09-01 01:42:06.184878+00	\N
msg-1756691204443-nepkiuwct	f5cd87a5-0f3e-406e-a8d7-c396361d0d4e	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:46:44.444+00	2025-09-01 01:46:44.448973+00	\N
msg-1756691204489-9z23sq49q	f5cd87a5-0f3e-406e-a8d7-c396361d0d4e	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:46:44.49+00	2025-09-01 01:46:44.494876+00	\N
msg-1756691212260-v0kpu9alj	f5cd87a5-0f3e-406e-a8d7-c396361d0d4e	Привет! Давай начнем! Бороскавор.	user	minio://audio-files/f5cd87a5-0f3e-406e-a8d7-c396361d0d4e_recording_1756691212260.webm	-1	2025-09-01 01:46:55.815+00	2025-09-01 01:46:55.820118+00	\N
msg-1756691233586-8eddkz9kb	f5cd87a5-0f3e-406e-a8d7-c396361d0d4e	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:47:13.586+00	2025-09-01 01:47:13.592925+00	\N
msg-1756691746289-xzxzcb9pt	f14d28f8-66f1-4561-868f-33562e86667b	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:55:46.289+00	2025-09-01 01:55:46.293903+00	\N
msg-1756691746330-rpfoog15v	f14d28f8-66f1-4561-868f-33562e86667b	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:55:46.33+00	2025-09-01 01:55:46.33735+00	\N
msg-1756691757814-r98k841j3	f14d28f8-66f1-4561-868f-33562e86667b	Привет! Давай начнём.	user	minio://audio-files/f14d28f8-66f1-4561-868f-33562e86667b_recording_1756691757814.webm	-1	2025-09-01 01:56:00.981+00	2025-09-01 01:56:00.985376+00	\N
msg-1756691778344-oov1krvmy	f14d28f8-66f1-4561-868f-33562e86667b	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:56:18.344+00	2025-09-01 01:56:18.359013+00	\N
msg-1756691945747-f3i19ryk1	deefc08e-a5bd-46ff-9867-55ad65b926bd	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 01:59:05.747+00	2025-09-01 01:59:05.75302+00	\N
msg-1756691945861-oe53azuob	deefc08e-a5bd-46ff-9867-55ad65b926bd	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:59:05.861+00	2025-09-01 01:59:05.865987+00	\N
msg-1756691950808-wg11p0t9t	deefc08e-a5bd-46ff-9867-55ad65b926bd	Привет!	user	minio://audio-files/deefc08e-a5bd-46ff-9867-55ad65b926bd_recording_1756691950809.webm	-1	2025-09-01 01:59:13.337+00	2025-09-01 01:59:13.343211+00	\N
msg-1756691971613-on9zvclsn	deefc08e-a5bd-46ff-9867-55ad65b926bd	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 01:59:31.614+00	2025-09-01 01:59:31.62233+00	\N
msg-1756692418356-kb1ab6ee8	deefc08e-a5bd-46ff-9867-55ad65b926bd	Давай проверим еще раз. как это работает.	user	minio://audio-files/deefc08e-a5bd-46ff-9867-55ad65b926bd_recording_1756692418356.webm	0	2025-09-01 02:07:01.565+00	2025-09-01 02:07:01.574651+00	\N
msg-1756692440448-t8ib4bd7d	deefc08e-a5bd-46ff-9867-55ad65b926bd	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:07:20.448+00	2025-09-01 02:07:20.454143+00	\N
msg-1756692807894-69kvtjmhi	4405afed-77ba-4097-b747-a6a943bffdb5	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 02:13:27.894+00	2025-09-01 02:13:27.900005+00	\N
msg-1756692807968-vojveqq5i	4405afed-77ba-4097-b747-a6a943bffdb5	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:13:27.968+00	2025-09-01 02:13:27.974227+00	\N
msg-1756692814064-jsz86ojld	4405afed-77ba-4097-b747-a6a943bffdb5	Просто 2345.	user	minio://audio-files/4405afed-77ba-4097-b747-a6a943bffdb5_recording_1756692814064.webm	-1	2025-09-01 02:13:36.499+00	2025-09-01 02:13:36.502785+00	\N
msg-1756692882299-asbxmfv93	4405afed-77ba-4097-b747-a6a943bffdb5	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:14:42.3+00	2025-09-01 02:14:42.30492+00	\N
msg-1756693168454-ctb9h78pl	7512198e-12c1-40b7-a1dd-f43304763bd2	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 02:19:28.455+00	2025-09-01 02:19:28.458628+00	\N
msg-1756693168492-npln7z5gw	7512198e-12c1-40b7-a1dd-f43304763bd2	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:19:28.492+00	2025-09-01 02:19:28.496802+00	\N
msg-1756693177570-hhcwa2xvu	7512198e-12c1-40b7-a1dd-f43304763bd2	Всем по-чем. 22 привет.	user	minio://audio-files/7512198e-12c1-40b7-a1dd-f43304763bd2_recording_1756693177570.webm	-1	2025-09-01 02:19:41.628+00	2025-09-01 02:19:41.632293+00	\N
msg-1756693247199-nw6ngcn0z	7512198e-12c1-40b7-a1dd-f43304763bd2	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:20:47.199+00	2025-09-01 02:20:47.204992+00	\N
msg-1756693308608-r6xs874sn	7512198e-12c1-40b7-a1dd-f43304763bd2	Что-то у тебя не получилось.	user	minio://audio-files/7512198e-12c1-40b7-a1dd-f43304763bd2_recording_1756693308608.webm	0	2025-09-01 02:21:51.471+00	2025-09-01 02:21:51.474797+00	\N
msg-1756693377441-ussj04rqy	7512198e-12c1-40b7-a1dd-f43304763bd2	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:22:57.441+00	2025-09-01 02:22:57.447655+00	\N
msg-1756693703130-jf3w7rk0d	8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-01 02:28:23.13+00	2025-09-01 02:28:23.134506+00	\N
msg-1756693703169-0uur62qo7	8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:28:23.169+00	2025-09-01 02:28:23.173219+00	\N
msg-1756693713818-r3sv7xzxc	8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87	один. Два.	user	minio://audio-files/8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87_recording_1756693713818.webm	-1	2025-09-01 02:28:39.075+00	2025-09-01 02:28:39.079561+00	\N
msg-1756693784621-vswi6atn9	8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-01 02:29:44.622+00	2025-09-01 02:29:44.626538+00	\N
msg-1756851602137-tzhnncc5f	6c7f12f9-900e-4923-a77f-2343fde92706	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 22:20:02.138+00	2025-09-02 22:20:02.143994+00	\N
msg-1756851602187-rl4b9n85n	6c7f12f9-900e-4923-a77f-2343fde92706	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:20:02.187+00	2025-09-02 22:20:02.191988+00	\N
msg-1756851615320-g53uzqy6j	6c7f12f9-900e-4923-a77f-2343fde92706	Could not transcribe audio	user	minio://audio-files/6c7f12f9-900e-4923-a77f-2343fde92706_recording_1756851615320.webm	0	2025-09-02 22:20:41.668+00	2025-09-02 22:20:41.674139+00	\N
msg-1756851707092-e7if0ou64	6c7f12f9-900e-4923-a77f-2343fde92706	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:21:47.093+00	2025-09-02 22:21:47.10022+00	\N
msg-1756851884868-i379d6vtm	6c7f12f9-900e-4923-a77f-2343fde92706	Рас два. Опять у нас что-то не работает.	user	minio://audio-files/6c7f12f9-900e-4923-a77f-2343fde92706_recording_1756851884868.webm	-1	2025-09-02 22:24:48.308+00	2025-09-02 22:24:48.317655+00	\N
msg-1756851953891-23wbihc07	6c7f12f9-900e-4923-a77f-2343fde92706	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:25:53.891+00	2025-09-02 22:25:53.89974+00	\N
msg-1756852424914-g0030vuu1	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 22:33:44.914+00	2025-09-02 22:33:44.919043+00	\N
msg-1756852424956-w1gzz2w50	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:33:44.956+00	2025-09-02 22:33:44.962176+00	\N
msg-1756852433779-mhlo5y0cz	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	какие технологии тебя интересуют.	user	minio://audio-files/d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3_recording_1756852433779.webm	0	2025-09-02 22:33:54.987+00	2025-09-02 22:33:54.992888+00	\N
msg-1756852516763-7u4vg2rsu	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:35:16.764+00	2025-09-02 22:35:16.768077+00	\N
msg-1756852717748-vjigaszt5	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	Честно, я вообще не понимаю, что ты от меня хочешь.	user	minio://audio-files/d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3_recording_1756852717748.webm	0	2025-09-02 22:38:40.481+00	2025-09-02 22:38:40.490444+00	\N
msg-1756852822364-wxz8kjpml	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:40:22.365+00	2025-09-02 22:40:22.370402+00	\N
msg-1756853064537-r1pc6tctd	988d6943-2d17-48f7-812a-830a6ea12fb4	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 22:44:24.537+00	2025-09-02 22:44:24.543411+00	\N
msg-1756853064582-cyed4h9yw	988d6943-2d17-48f7-812a-830a6ea12fb4	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:44:24.582+00	2025-09-02 22:44:24.58794+00	\N
msg-1756853217202-7e7soozwa	988d6943-2d17-48f7-812a-830a6ea12fb4	что-то я не дождался тебе генераций, ты вообще работаешь.	user	minio://audio-files/988d6943-2d17-48f7-812a-830a6ea12fb4_recording_1756853217202.webm	0	2025-09-02 22:46:58.784+00	2025-09-02 22:46:58.788133+00	\N
msg-1756853312957-1fvq9t1dl	988d6943-2d17-48f7-812a-830a6ea12fb4	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:48:32.957+00	2025-09-02 22:48:32.96488+00	\N
msg-1756853630974-zm5i5msk5	8a3d7e46-2986-4002-9211-891c507f1329	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 22:53:50.974+00	2025-09-02 22:53:50.978802+00	\N
msg-1756853631015-kg5onwbfk	8a3d7e46-2986-4002-9211-891c507f1329	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:53:51.015+00	2025-09-02 22:53:51.02021+00	\N
msg-1756853639337-58qp787o0	8a3d7e46-2986-4002-9211-891c507f1329	Привет! Я ничего не знаю. от требованиях.	user	minio://audio-files/8a3d7e46-2986-4002-9211-891c507f1329_recording_1756853639337.webm	0	2025-09-02 22:54:03.272+00	2025-09-02 22:54:03.276489+00	\N
msg-1756853713696-dxzxon0up	8a3d7e46-2986-4002-9211-891c507f1329	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 22:55:13.696+00	2025-09-02 22:55:13.702407+00	\N
msg-1756854954755-2vvzf008m	afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 23:15:54.755+00	2025-09-02 23:15:54.759827+00	\N
msg-1756854954795-1n3z2vhs0	afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 23:15:54.795+00	2025-09-02 23:15:54.799025+00	\N
msg-1756855083553-mmphe5s66	afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db	Так, чуть ничего не понятно.	user	minio://audio-files/afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db_recording_1756855083553.webm	-1	2025-09-02 23:18:04.912+00	2025-09-02 23:18:04.917634+00	\N
msg-1756855144029-qj4mfu9w4	afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 23:19:04.029+00	2025-09-02 23:19:04.036558+00	\N
msg-1756855777286-b87mryhfi	3538c3c2-5583-4034-a755-bbcdc555534f	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 23:29:37.286+00	2025-09-02 23:29:37.293381+00	\N
msg-1756855777353-g1ptq7j0w	3538c3c2-5583-4034-a755-bbcdc555534f	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 23:29:37.353+00	2025-09-02 23:29:37.357168+00	\N
msg-1756857188252-b33c42io1	688a2ae9-c388-4068-b370-305442187aa5	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-02 23:53:08.252+00	2025-09-02 23:53:08.258841+00	\N
msg-1756857188320-hesqtc3mj	688a2ae9-c388-4068-b370-305442187aa5	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 23:53:08.32+00	2025-09-02 23:53:08.325769+00	\N
msg-1756857194324-9ijry6zgk	688a2ae9-c388-4068-b370-305442187aa5	Привет, расскажи мне в оканстве.	user	minio://audio-files/688a2ae9-c388-4068-b370-305442187aa5_recording_1756857194324.webm	0	2025-09-02 23:53:18.337+00	2025-09-02 23:53:18.341441+00	\N
msg-1756857255376-02rc3pc2x	688a2ae9-c388-4068-b370-305442187aa5	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-02 23:54:15.376+00	2025-09-02 23:54:15.38219+00	\N
msg-1756857730993-mu7biyk05	f336f13d-065b-4465-a06d-73bde6cef558	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?	avatar	\N	\N	2025-09-03 00:02:10.993+00	2025-09-03 00:02:11.001244+00	\N
msg-1756857731069-4e27d6trb	f336f13d-065b-4465-a06d-73bde6cef558	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:02:11.069+00	2025-09-03 00:02:11.074871+00	\N
msg-1756858688092-ymwne8fwo	8ea0a596-7bea-4690-8a55-545ae125cb79	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-03 00:18:08.092+00	2025-09-03 00:18:08.09931+00	\N
msg-1756858756651-r9fyp4cvd	8ea0a596-7bea-4690-8a55-545ae125cb79	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:19:16.652+00	2025-09-03 00:19:16.656986+00	\N
msg-1756858830464-xos4abiub	8ea0a596-7bea-4690-8a55-545ae125cb79	А расскажи мне... О! пока не си.	user	minio://audio-files/8ea0a596-7bea-4690-8a55-545ae125cb79_recording_1756858830464.webm	-1	2025-09-03 00:20:33.483+00	2025-09-03 00:20:33.486706+00	\N
msg-1756858895690-yuikn7jpy	8ea0a596-7bea-4690-8a55-545ae125cb79	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:21:35.691+00	2025-09-03 00:21:35.695309+00	\N
msg-1756858914746-tt4zojz65	8ea0a596-7bea-4690-8a55-545ae125cb79	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:21:54.746+00	2025-09-03 00:21:54.751386+00	\N
msg-1756858948807-zqdspvin8	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-03 00:22:28.807+00	2025-09-03 00:22:28.812524+00	\N
msg-1756859010447-14nzccky2	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:23:30.447+00	2025-09-03 00:23:30.460046+00	\N
msg-1756859077616-9s0vbv9yw	7a80becf-5f55-4231-b65f-0272ecb5e8c1	А расскажем мне о собой. по кончену.	user	minio://audio-files/7a80becf-5f55-4231-b65f-0272ecb5e8c1_recording_1756859077616.webm	-1	2025-09-03 00:24:39.91+00	2025-09-03 00:24:39.913349+00	\N
msg-1756859140674-ayuis6rn8	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:25:40.674+00	2025-09-03 00:25:40.681072+00	\N
msg-1756859204586-m6cb6xgd3	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:26:44.586+00	2025-09-03 00:26:44.590158+00	\N
msg-1756859265757-j0mnnrl76	7a80becf-5f55-4231-b65f-0272ecb5e8c1	у меня большую подработку.	user	minio://audio-files/7a80becf-5f55-4231-b65f-0272ecb5e8c1_recording_1756859265757.webm	-1	2025-09-03 00:27:47.057+00	2025-09-03 00:27:47.061793+00	\N
msg-1756859336944-cf4lorf5p	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:28:56.944+00	2025-09-03 00:28:56.957344+00	\N
msg-1756859391019-btkorqoh1	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:29:51.019+00	2025-09-03 00:29:51.023905+00	\N
msg-1756859467543-67055wuyd	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Could not transcribe audio	user	minio://audio-files/7a80becf-5f55-4231-b65f-0272ecb5e8c1_recording_1756859467543.webm	\N	2025-09-03 00:31:07.804+00	2025-09-03 00:31:07.80801+00	\N
msg-1756859530419-isirr2ggp	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:32:10.419+00	2025-09-03 00:32:10.424507+00	\N
msg-1756859584341-4qkwkmx7p	7a80becf-5f55-4231-b65f-0272ecb5e8c1	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:33:04.341+00	2025-09-03 00:33:04.346922+00	\N
msg-1756860081105-8esryxjrw	dae0342d-3e1a-4094-9fbb-42f68b9257e6	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-03 00:41:21.105+00	2025-09-03 00:41:21.110909+00	\N
msg-1756860086202-a3vrdilxl	dae0342d-3e1a-4094-9fbb-42f68b9257e6	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 00:41:26.202+00	2025-09-03 00:41:26.206804+00	\N
msg-1756896725902-i91gdaf2a	eb4d49d9-a3f5-4357-8229-b2aaf89a5f10	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-03 10:52:05.902+00	2025-09-03 10:52:05.90904+00	\N
msg-1756896796472-o9w0ta13m	eb4d49d9-a3f5-4357-8229-b2aaf89a5f10	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 10:53:16.472+00	2025-09-03 10:53:16.476712+00	\N
msg-1756925502164-1g1d17pgi	4fc694e8-bcc9-4b4e-a074-4266ece4873f	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-03 18:51:42.164+00	2025-09-03 18:51:42.169826+00	\N
msg-1756925571230-f0zke87jf	4fc694e8-bcc9-4b4e-a074-4266ece4873f	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 18:52:51.23+00	2025-09-03 18:52:51.239044+00	\N
msg-1756925635265-fxx8puaok	d9d06d6a-9d2a-42df-8fac-cc572c69a580	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-03 18:53:55.265+00	2025-09-03 18:53:55.26931+00	\N
msg-1756925687726-iz3ee4zxt	d9d06d6a-9d2a-42df-8fac-cc572c69a580	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 18:54:47.726+00	2025-09-03 18:54:47.733884+00	\N
msg-1756925781573-pa5ces1mc	d9d06d6a-9d2a-42df-8fac-cc572c69a580	Привет, я ничего не знаю про твою вакансию, вообще о чем-то разговариваешь, кто ты такая. Н.Закомолдина	user	minio://audio-files/d9d06d6a-9d2a-42df-8fac-cc572c69a580_recording_1756925781573.webm	0	2025-09-03 18:57:40.491+00	2025-09-03 18:57:40.498936+00	\N
msg-1756925949586-bhetqdiri	d9d06d6a-9d2a-42df-8fac-cc572c69a580	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-03 18:59:09.586+00	2025-09-03 18:59:09.596284+00	\N
msg-1757274000618-5xe9mcnov	c6942653-d339-40c1-9594-9084dd46b10f	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-07 19:40:00.618+00	2025-09-07 19:40:00.624457+00	\N
msg-1757274059247-6csvwurbl	c6942653-d339-40c1-9594-9084dd46b10f	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-07 19:40:59.247+00	2025-09-07 19:40:59.251909+00	\N
msg-1757284434596-8vjcvk18a	aba2d9c0-8e50-4212-bd36-46843f1e2113	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-07 22:33:54.596+00	2025-09-07 22:33:54.602791+00	\N
msg-1757284486846-0j5toqv38	aba2d9c0-8e50-4212-bd36-46843f1e2113	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-07 22:34:46.846+00	2025-09-07 22:34:46.850718+00	\N
msg-1757347488006-hco204gsl	6912a995-49ad-40e4-96e2-48e1a4f113c0	Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыков. Готовы начать?	avatar	\N	\N	2025-09-08 16:04:48.006+00	2025-09-08 16:04:48.014522+00	\N
msg-1757347545735-o1sjdhsak	6912a995-49ad-40e4-96e2-48e1a4f113c0	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	avatar	\N	\N	2025-09-08 16:05:45.735+00	2025-09-08 16:05:45.738402+00	\N
\.


--
-- Data for Name: qa; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.qa (id, session_id, step_no, question_id, question_text, answer_text, audio_url, tone, passed, created_at, updated_at) FROM stdin;
1	SESS_001	1	Q_FASTAPI_01	Расскажите про ваш опыт работы с FastAPI...	Я работал с FastAPI в нескольких проектах. Использовал Depends для внедрения зависимостей, BackgroundTasks для асинхронных задач, Pydantic для валидации данных. Также интегрировал с PostgreSQL через SQLAlchemy.	https://minio:9000/interview-audio/answer_001.wav	positive	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
2	SESS_001	2	Q_ASYNCIO_01	Объясните, как работает асинхронное программирование...	Асинхронное программирование позволяет выполнять операции без блокировки. Использую async/await, asyncio.gather для параллельного выполнения задач.	https://minio:9000/interview-audio/answer_002.wav	neutral	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
3	SESS_001	3	Q_DATABASE_01	Опишите ваш опыт работы с базами данных...	Работал с PostgreSQL, Redis, MongoDB. Использую миграции, индексы для оптимизации запросов.	https://minio:9000/interview-audio/answer_003.wav	positive	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
4	SESS_001	4	Q_TESTING_01	Расскажите о вашем подходе к тестированию...	Пишу unit-тесты с pytest, интеграционные тесты, использую моки и фикстуры.	https://minio:9000/interview-audio/answer_004.wav	neutral	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
5	SESS_001	5	Q_MICROSERVICES_01	Каков ваш опыт работы с микросервисной архитектурой...	Работал с Docker, Kubernetes, сервис-мешами. Решал проблемы с сетевой связностью и мониторингом.	https://minio:9000/interview-audio/answer_005.wav	positive	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
6	SESS_001	6	Q_DEPLOYMENT_01	Опишите процесс деплоя приложений...	Использую CI/CD пайплайны, Docker контейнеры, автоматическое развертывание через GitLab CI.	https://minio:9000/interview-audio/answer_006.wav	neutral	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
7	SESS_001	7	Q_PROBLEM_SOLVING_01	Опишите сложную техническую задачу...	Оптимизировал медленные запросы к БД, использовал кэширование, переписал критические участки кода.	https://minio:9000/interview-audio/answer_007.wav	positive	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
8	SESS_001	8	Q_TEAMWORK_01	Расскажите о вашем опыте работы в команде...	Работаю в команде из 5 разработчиков, участвую в code review, помогаю коллегам с техническими вопросами.	https://minio:9000/interview-audio/answer_008.wav	positive	t	2025-08-27 16:41:06.416716+00	2025-08-27 16:41:06.416716+00
17	c55aab56-a42f-45a7-afd8-59f4b81383b7	1	\N	Расскажите о вашем опыте работы с FastAPI	У меня есть опыт работы с FastAPI около 2 лет. Я создавал REST API для различных проектов, включая систему управления пользователями и интеграцию с внешними сервисами.	minio://audio-files/test_audio.webm	neutral	f	2025-08-31 18:56:41.927592+00	2025-08-31 18:56:41.92565+00
18	ad597e46-2ba9-4482-bda9-b2253d60ecab	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Дай готов!	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598837474.webm	neutral	f	2025-08-31 19:01:33.172316+00	2025-08-31 19:01:33.171439+00
19	ad597e46-2ba9-4482-bda9-b2253d60ecab	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Я вилния скройку крупных паций.	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598849785.webm	neutral	f	2025-08-31 19:01:33.734361+00	2025-08-31 19:01:33.733346+00
20	ad597e46-2ba9-4482-bda9-b2253d60ecab	3	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	это крупные проекты.	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598863322.webm	neutral	f	2025-08-31 19:01:34.302678+00	2025-08-31 19:01:34.301119+00
21	ad597e46-2ba9-4482-bda9-b2253d60ecab	4	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	анализировал требования и составлял документы.	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598880467.webm	neutral	f	2025-08-31 19:01:34.866836+00	2025-08-31 19:01:34.865442+00
22	c55aab56-a42f-45a7-afd8-59f4b81383b7	2	\N	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	Аудио запись не удалось транскрибировать	minio://audio-files/c55aab56-a42f-45a7-afd8-59f4b81383b7_recording_1756572872202.webm	neutral	f	2025-08-31 19:04:19.685237+00	2025-08-31 19:04:19.683719+00
23	ad597e46-2ba9-4482-bda9-b2253d60ecab	5	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Дай готов!	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598837474.webm	neutral	f	2025-08-31 19:04:21.252189+00	2025-08-31 19:04:21.251225+00
24	ad597e46-2ba9-4482-bda9-b2253d60ecab	6	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Я вилния скройку крупных паций.	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598849785.webm	neutral	f	2025-08-31 19:04:21.793003+00	2025-08-31 19:04:21.792287+00
25	ad597e46-2ba9-4482-bda9-b2253d60ecab	7	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	это крупные проекты.	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598863322.webm	neutral	f	2025-08-31 19:04:22.325167+00	2025-08-31 19:04:22.324573+00
26	ad597e46-2ba9-4482-bda9-b2253d60ecab	8	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	анализировал требования и составлял документы.	minio://audio-files/ad597e46-2ba9-4482-bda9-b2253d60ecab_recording_1756598880467.webm	neutral	f	2025-08-31 19:04:22.853469+00	2025-08-31 19:04:22.853038+00
27	f26a8d59-b340-4a31-b07f-650f89818097	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	А я не знаю, какая бы кончая какие технологии.	minio://audio-files/f26a8d59-b340-4a31-b07f-650f89818097_recording_1756685977801.webm	neutral	f	2025-09-01 00:19:45.244785+00	2025-09-01 00:19:45.242934+00
28	dd299d81-63b2-42f5-a10f-8af6bb8176d7	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет!	minio://audio-files/dd299d81-63b2-42f5-a10f-8af6bb8176d7_recording_1756686459129.webm	neutral	f	2025-09-01 00:27:45.050414+00	2025-09-01 00:27:45.049328+00
29	87240571-1983-4a50-83a9-f7859a04ab30	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	СПОКОЙНАЯ МУЗЫКА Привет!	minio://audio-files/87240571-1983-4a50-83a9-f7859a04ab30_recording_1756686682229.webm	neutral	f	2025-09-01 00:31:27.544353+00	2025-09-01 00:31:27.543872+00
30	87240571-1983-4a50-83a9-f7859a04ab30	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	А я не помню, как это.	minio://audio-files/87240571-1983-4a50-83a9-f7859a04ab30_recording_1756686712875.webm	neutral	f	2025-09-01 00:31:58.803511+00	2025-09-01 00:31:58.802942+00
31	87240571-1983-4a50-83a9-f7859a04ab30	3	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	у меня в Excel.	minio://audio-files/87240571-1983-4a50-83a9-f7859a04ab30_recording_1756686733966.webm	neutral	f	2025-09-01 00:32:18.729601+00	2025-09-01 00:32:18.728612+00
32	85b86496-6fcd-4bbc-98d0-2f4c5dfb6504	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Раз, два, три, четыре, пять.	minio://audio-files/85b86496-6fcd-4bbc-98d0-2f4c5dfb6504_recording_1756686864269.webm	neutral	f	2025-09-01 00:34:27.312337+00	2025-09-01 00:34:27.311467+00
33	b7a7ee54-5ae5-45fc-8ad5-9f51ff109815	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет! Ичё?	minio://audio-files/b7a7ee54-5ae5-45fc-8ad5-9f51ff109815_recording_1756688887550.webm	neutral	f	2025-09-01 01:08:16.208633+00	2025-09-01 01:08:16.20719+00
34	c5f1edfb-4f41-4be9-b3b9-25f3f96c2181	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Рас? 3 4 5	minio://audio-files/c5f1edfb-4f41-4be9-b3b9-25f3f96c2181_recording_1756689514835.webm	neutral	f	2025-09-01 01:18:42.784279+00	2025-09-01 01:18:42.782999+00
35	f6265ee7-76f4-41f3-bec3-228982c39989	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет, раз-два-три. 4,5,6,7,8,1,25 А.Синецкая	minio://audio-files/f6265ee7-76f4-41f3-bec3-228982c39989_recording_1756690196515.webm	neutral	f	2025-09-01 01:30:04.293843+00	2025-09-01 01:30:04.29201+00
36	09a2d860-1f50-4ef2-b672-758e4e5f2251	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Рас. Два. 3,4,5,6	minio://audio-files/09a2d860-1f50-4ef2-b672-758e4e5f2251_recording_1756690901472.webm	neutral	f	2025-09-01 01:41:50.143709+00	2025-09-01 01:41:50.141446+00
37	f5cd87a5-0f3e-406e-a8d7-c396361d0d4e	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет! Давай начнем! Бороскавор.	minio://audio-files/f5cd87a5-0f3e-406e-a8d7-c396361d0d4e_recording_1756691212260.webm	neutral	f	2025-09-01 01:46:57.732391+00	2025-09-01 01:46:57.731178+00
38	f14d28f8-66f1-4561-868f-33562e86667b	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет! Давай начнём.	minio://audio-files/f14d28f8-66f1-4561-868f-33562e86667b_recording_1756691757814.webm	neutral	f	2025-09-01 01:56:02.928085+00	2025-09-01 01:56:02.926859+00
39	deefc08e-a5bd-46ff-9867-55ad65b926bd	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет!	minio://audio-files/deefc08e-a5bd-46ff-9867-55ad65b926bd_recording_1756691950809.webm	neutral	f	2025-09-01 01:59:15.679094+00	2025-09-01 01:59:15.677761+00
40	deefc08e-a5bd-46ff-9867-55ad65b926bd	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Давай проверим еще раз. как это работает.	minio://audio-files/deefc08e-a5bd-46ff-9867-55ad65b926bd_recording_1756692418356.webm	neutral	f	2025-09-01 02:07:03.584763+00	2025-09-01 02:07:03.579719+00
41	4405afed-77ba-4097-b747-a6a943bffdb5	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Просто 2345.	minio://audio-files/4405afed-77ba-4097-b747-a6a943bffdb5_recording_1756692814064.webm	neutral	f	2025-09-01 02:13:38.352322+00	2025-09-01 02:13:38.351549+00
42	7512198e-12c1-40b7-a1dd-f43304763bd2	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Всем по-чем. 22 привет.	minio://audio-files/7512198e-12c1-40b7-a1dd-f43304763bd2_recording_1756693177570.webm	neutral	f	2025-09-01 02:19:43.508102+00	2025-09-01 02:19:43.506804+00
43	7512198e-12c1-40b7-a1dd-f43304763bd2	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Что-то у тебя не получилось.	minio://audio-files/7512198e-12c1-40b7-a1dd-f43304763bd2_recording_1756693308608.webm	neutral	f	2025-09-01 02:21:53.526395+00	2025-09-01 02:21:53.525309+00
44	8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	один. Два.	minio://audio-files/8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87_recording_1756693713818.webm	neutral	f	2025-09-01 02:28:40.895871+00	2025-09-01 02:28:40.895066+00
45	6c7f12f9-900e-4923-a77f-2343fde92706	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Could not transcribe audio	minio://audio-files/6c7f12f9-900e-4923-a77f-2343fde92706_recording_1756851615320.webm	neutral	f	2025-09-02 22:20:43.338212+00	2025-09-02 22:20:43.334125+00
46	6c7f12f9-900e-4923-a77f-2343fde92706	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Рас два. Опять у нас что-то не работает.	minio://audio-files/6c7f12f9-900e-4923-a77f-2343fde92706_recording_1756851884868.webm	neutral	f	2025-09-02 22:24:50.119885+00	2025-09-02 22:24:50.113235+00
47	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	какие технологии тебя интересуют.	minio://audio-files/d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3_recording_1756852433779.webm	neutral	f	2025-09-02 22:33:56.792932+00	2025-09-02 22:33:56.79191+00
48	d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Честно, я вообще не понимаю, что ты от меня хочешь.	minio://audio-files/d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3_recording_1756852717748.webm	neutral	f	2025-09-02 22:38:42.203131+00	2025-09-02 22:38:42.200338+00
49	988d6943-2d17-48f7-812a-830a6ea12fb4	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	что-то я не дождался тебе генераций, ты вообще работаешь.	minio://audio-files/988d6943-2d17-48f7-812a-830a6ea12fb4_recording_1756853217202.webm	neutral	f	2025-09-02 22:47:00.42947+00	2025-09-02 22:47:00.428032+00
50	8a3d7e46-2986-4002-9211-891c507f1329	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет! Я ничего не знаю. от требованиях.	minio://audio-files/8a3d7e46-2986-4002-9211-891c507f1329_recording_1756853639337.webm	neutral	f	2025-09-02 22:54:05.254864+00	2025-09-02 22:54:05.252989+00
51	afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Так, чуть ничего не понятно.	minio://audio-files/afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db_recording_1756855083553.webm	neutral	f	2025-09-02 23:18:06.458568+00	2025-09-02 23:18:06.456792+00
52	688a2ae9-c388-4068-b370-305442187aa5	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет, расскажи мне в оканстве.	minio://audio-files/688a2ae9-c388-4068-b370-305442187aa5_recording_1756857194324.webm	neutral	f	2025-09-02 23:53:19.926074+00	2025-09-02 23:53:19.924049+00
53	8ea0a596-7bea-4690-8a55-545ae125cb79	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	А расскажи мне... О! пока не си.	minio://audio-files/8ea0a596-7bea-4690-8a55-545ae125cb79_recording_1756858830464.webm	neutral	f	2025-09-03 00:20:35.150876+00	2025-09-03 00:20:35.148987+00
54	7a80becf-5f55-4231-b65f-0272ecb5e8c1	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	А расскажем мне о собой. по кончену.	minio://audio-files/7a80becf-5f55-4231-b65f-0272ecb5e8c1_recording_1756859077616.webm	neutral	f	2025-09-03 00:24:41.552191+00	2025-09-03 00:24:41.551279+00
55	7a80becf-5f55-4231-b65f-0272ecb5e8c1	2	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	у меня большую подработку.	minio://audio-files/7a80becf-5f55-4231-b65f-0272ecb5e8c1_recording_1756859265757.webm	neutral	f	2025-09-03 00:27:48.883735+00	2025-09-03 00:27:48.883008+00
56	7a80becf-5f55-4231-b65f-0272ecb5e8c1	3	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Could not transcribe audio	minio://audio-files/7a80becf-5f55-4231-b65f-0272ecb5e8c1_recording_1756859467543.webm	neutral	f	2025-09-03 00:31:09.408477+00	2025-09-03 00:31:09.407227+00
57	d9d06d6a-9d2a-42df-8fac-cc572c69a580	1	\N	Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.	Привет, я ничего не знаю про твою вакансию, вообще о чем-то разговариваешь, кто ты такая. Н.Закомолдина	minio://audio-files/d9d06d6a-9d2a-42df-8fac-cc572c69a580_recording_1756925781573.webm	neutral	f	2025-09-03 18:57:42.077858+00	2025-09-03 18:57:42.076974+00
\.


--
-- Data for Name: qa_scores; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.qa_scores (id, qa_id, criterion_id, score, evidence, red_flag, created_at, updated_at) FROM stdin;
1	1	FASTAPI	0.90	Упоминает Depends, BackgroundTasks, Pydantic - показывает глубокое знание фреймворка	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
2	1	ASYNCIO	0.70	Понимает асинхронность, но не показывает глубоких знаний	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
3	2	ASYNCIO	0.80	Правильно объясняет async/await, упоминает asyncio.gather	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
4	3	DATABASE	0.85	Опыт с разными БД, понимает миграции и индексы	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
5	4	TESTING	0.75	Знает pytest, понимает разные типы тестов	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
6	5	MICROSERVICES	0.80	Опыт с Docker, Kubernetes, понимает проблемы архитектуры	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
7	5	PROBLEM_SOLVING	0.70	Показывает способность решать технические проблемы	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
8	6	DEPLOYMENT	0.70	Знает CI/CD, Docker, автоматизацию	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
9	7	PROBLEM_SOLVING	0.90	Конкретный пример оптимизации с измеримыми результатами	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
10	7	TEAMWORK	0.60	Упоминает командную работу, но не детализирует	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
11	8	TEAMWORK	0.80	Конкретные примеры работы в команде, code review	f	2025-08-27 16:41:06.419593+00	2025-08-27 16:41:06.419593+00
12	1	FASTAPI	0.90	Упоминает Depends, BackgroundTasks, Pydantic - показывает глубокое знание фреймворка	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
13	1	ASYNCIO	0.70	Понимает асинхронность, но не показывает глубоких знаний	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
14	2	ASYNCIO	0.80	Правильно объясняет async/await, упоминает asyncio.gather	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
15	3	DATABASE	0.85	Опыт с разными БД, понимает миграции и индексы	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
16	4	TESTING	0.75	Знает pytest, понимает разные типы тестов	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
17	5	MICROSERVICES	0.80	Опыт с Docker, Kubernetes, понимает проблемы архитектуры	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
18	5	PROBLEM_SOLVING	0.70	Показывает способность решать технические проблемы	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
19	6	DEPLOYMENT	0.70	Знает CI/CD, Docker, автоматизацию	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
20	7	PROBLEM_SOLVING	0.90	Конкретный пример оптимизации с измеримыми результатами	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
21	7	TEAMWORK	0.60	Упоминает командную работу, но не детализирует	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
22	8	TEAMWORK	0.80	Конкретные примеры работы в команде, code review	f	2025-08-30 14:53:56.611959+00	2025-08-30 14:53:56.611959+00
\.


--
-- Data for Name: question_criteria; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.question_criteria (question_id, criterion_id, weight, must_have, min_score, created_at) FROM stdin;
Q_FASTAPI_01	FASTAPI	0.80	t	0.70	2025-08-27 16:41:06.41268+00
Q_FASTAPI_01	ASYNCIO	0.20	f	0.00	2025-08-27 16:41:06.41268+00
Q_ASYNCIO_01	ASYNCIO	1.00	f	0.00	2025-08-27 16:41:06.41268+00
Q_DATABASE_01	DATABASE	1.00	f	0.00	2025-08-27 16:41:06.41268+00
Q_TESTING_01	TESTING	1.00	f	0.00	2025-08-27 16:41:06.41268+00
Q_MICROSERVICES_01	MICROSERVICES	0.70	f	0.00	2025-08-27 16:41:06.41268+00
Q_MICROSERVICES_01	PROBLEM_SOLVING	0.30	f	0.00	2025-08-27 16:41:06.41268+00
Q_DEPLOYMENT_01	DEPLOYMENT	1.00	f	0.00	2025-08-27 16:41:06.41268+00
Q_PROBLEM_SOLVING_01	PROBLEM_SOLVING	0.80	f	0.00	2025-08-27 16:41:06.41268+00
Q_PROBLEM_SOLVING_01	TEAMWORK	0.20	f	0.00	2025-08-27 16:41:06.41268+00
Q_TEAMWORK_01	TEAMWORK	1.00	f	0.00	2025-08-27 16:41:06.41268+00
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.questions (id, text, type, max_duration_s, created_at, updated_at, is_vacancy_specific, category, difficulty_level) FROM stdin;
Q_FASTAPI_01	Расскажите про ваш опыт работы с FastAPI. Какие проекты вы реализовали с использованием этого фреймворка?	text	120	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_ASYNCIO_01	Объясните, как работает асинхронное программирование в Python. Приведите примеры использования asyncio.	text	90	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_DATABASE_01	Опишите ваш опыт работы с базами данных. Какие СУБД вы использовали и в каких проектах?	text	100	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_TESTING_01	Расскажите о вашем подходе к тестированию кода. Какие виды тестов вы пишете?	text	80	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_MICROSERVICES_01	Каков ваш опыт работы с микросервисной архитектурой? Какие проблемы вы решали?	text	110	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_DEPLOYMENT_01	Опишите процесс деплоя приложений. Какие инструменты и технологии вы используете?	text	90	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_PROBLEM_SOLVING_01	Опишите сложную техническую задачу, которую вам приходилось решать. Как вы подходили к её решению?	text	120	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
Q_TEAMWORK_01	Расскажите о вашем опыте работы в команде. Как вы взаимодействуете с коллегами?	text	100	2025-08-27 16:41:06.406423+00	2025-08-30 14:50:21.118956+00	f	\N	medium
\.


--
-- Data for Name: resume_blocks; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.resume_blocks (id, resume_id, block_type, block_name, extracted_text, relevance_score, confidence_score, matched_requirements, missing_requirements, analysis_notes, created_at, extracted_keywords) FROM stdin;
BLOCK_E7A6DDEA	RESUME_912F63A4	personal_info	Personal Info	Русский - родной язык, английский - уровень B2 (средне-продвинутый).	50.00	80.00	\N	\N	\N	2025-08-30 23:44:02.814479+00	\N
BLOCK_B5305B09	RESUME_912F63A4	skills	Skills	Базовые знания серверного оборудования х86; опыт работы с LAN и SAN; навыки администрирования локальных сетей (MS Active Directory, DNS, DHCP); подготовка корпоративных образов ОС; управление антивирусной защитой (Kaspersky Security Center); сопровождение серверов печати; опыт работы с Windows, Linux, Mac OS; навыки первичной диагностики серверного оборудования; знание структурированных кабельных систем; уверенные навыки работы с Excel, Word, Visio.	50.00	50.00	\N	\N	No required skills specified	2025-08-30 23:44:02.814479+00	{}
BLOCK_28DDECF6	RESUME_D0A2DD98	skills	Skills	Базовые знания серверного оборудования х86, структурированных кабельных систем (медных и оптических), сетей передачи и хранения данных (LAN и SAN), центров обработки данных. Навык первичной диагностики серверного оборудования х86. Навыки настройки BIOS, BMC, RAID. Знание OSI, MikroTik, Cisco, SSH, Ubuntu, Windows Server. Прокладка кабелей, сборка серверов, настройка сетевых подключений.	50.00	50.00	\N	\N	No required skills specified	2025-08-30 23:44:35.875213+00	{}
BLOCK_88F84C4E	RESUME_D0A2DD98	experience	Experience	Январь 2025 - настоящее время (6 месяцев): Ростелеком - Центры Обработки Данных, Специалист ЦОД. Настройка и конфигурация серверного и телекоммуникационного оборудования (сервера, СХД, магнитно-ленточные хранилища, криптошлюзы, коммутаторы, межсетевые экраны). Сборка оборудования, замена и установка комплектующих, введение в эксплуатацию. Монтаж и установка стоек, сборка и разборка коммутационных линий в соответствии со стандартами. Оперативное решение инцидентов, участие в восстановительных работах.\n\nИюль 2024 - Январь 2025 (7 месяцев): Кронос, Инженер эксплуатации ЦОД. Настройка и установка дистрибутивов. Сборка, техобслуживание, проверка серверного оборудования. Прокладка кроссовых трасс, кабель-менеджмент, написание скриптов bash/python. Настройка сетевого и серверного оборудования, включая роутеры, принтеры, ПК.	85.00	85.00	\N	\N	{'relevant_years': 1, 'relevance_score': 85, 'key_achievements': ['Настройка и конфигурация серверного и телекоммуникационного оборудования', 'Оперативное решение инцидентов и участие в восстановительных работах', 'Написание скриптов на bash/python для автоматизации задач', 'Прокладка кроссовых трасс и кабель-менеджмент'], 'relevant_projects': ['Сборка и ввод в эксплуатацию серверного оборудования', 'Настройка сетевого оборудования, включая криптошлюзы и межсетевые экраны', 'Проведение технического обслуживания серверов и периферийного оборудования'], 'gaps': ['Отсутствие информации о конкретных достижениях, таких как улучшение показателей работы ЦОД', 'Нет упоминания о работе с облачными технологиями или виртуализацией, если это требуется вакансией', 'Недостаток данных о взаимодействии с клиентами или командной работе'], 'recommendations': ['Добавить конкретные примеры успешных проектов или улучшений, внесенных в работу ЦОД', 'Уточнить опыт работы с современными технологиями, такими как виртуализация, контейнеризация или облачные платформы', 'Подчеркнуть навыки работы в команде или взаимодействия с клиентами, если это важно для вакансии'], 'personal_info': {}, 'experience_analysis': {}, 'skills_analysis': {}, 'overall_assessment': {}}	2025-08-30 23:44:35.875213+00	{}
BLOCK_A10F8E4D	RESUME_D0A2DD98	education	Education	Среднее специальное образование (2019): Колледж Экономики и Права, специальность 'Экономика, Товароведение и экспертиза товаров'.	100.00	75.00	\N	\N	{'candidate_level': 'bachelor', 'required_level': 'bachelor', 'score': 100}	2025-08-30 23:44:35.875213+00	{}
BLOCK_44A407BA	RESUME_912F63A4	experience	Experience	Август 2024 - настоящее время: Ведущий специалист технической поддержки пользователей (фриланс) - Подготовка рабочих станций на Windows, Linux, Mac OS; устранение неисправностей, в том числе удаленно; работа с DHCP, DNS; разработка образов Windows и автоматических файлов ответов для массовой установки. Январь 2023 - Август 2024: Ведущий специалист по технической ИТ поддержке (Retail.tech) - Подготовка рабочих станций на Windows, Linux, Mac OS; администрирование локальной сети (MS Active Directory, DNS, DHCP); управление антивирусной защитой (Kaspersky Security Center); сопровождение серверов печати. Август 2017 - Май 2022: Senior IT Infrastructure Support Engineer (EPAM Systems Inc.) - Подготовка рабочих станций на Windows и Linux; инфраструктурная поддержка; управление сервером печати и устройствами. Апрель 2016 - Август 2017: Системный администратор (Авиакомпания S7) - Организация рабочих мест пользователей; администрирование локальной сети (MS Active Directory, DNS, DHCP); управление антивирусной защитой; сопровождение серверов печати. Январь 2015 - Сентябрь 2015: Системный администратор (Янтарь, фармацевтическая компания) - Администрирование локальной сети (MS Active Directory, DNS, DHCP); поддержка принт-серверов и печатающей техники. Октябрь 2010 - Ноябрь 2013: Ведущий специалист по эксплуатации информационных систем (X5, группа компаний) - Администрирование локальной сети (MS Active Directory, DNS, DHCP); поддержка серверов печати; внедрение MS Windows Deployment Server для клонирования образов по сети. Октябрь 2009 - Июль 2010: Специалист технической поддержки пользователей (ОАО Завод) - Подготовка корпоративных образов ОС; поддержка серверов на базе Windows Server/Windows Server 2008. Август 2004 - Ноябрь 2008: Специалист технической поддержки пользователей (Альянс Банк, АО) - Поддержка пользователей офиса и ИТ оборудования банка.	80.00	85.00	\N	\N	{'relevant_years': '19', 'relevance_score': '80', 'key_achievements': ['Подготовка рабочих станций на Windows, Linux и Mac OS', 'Администрирование локальной сети (MS Active Directory, DNS, DHCP)', 'Управление антивирусной защитой (Kaspersky Security Center)', 'Разработка образов Windows и автоматических файлов ответов для массовой установки', 'Внедрение MS Windows Deployment Server для клонирования образов по сети'], 'relevant_projects': ['Разработка и внедрение образов Windows для массовой установки', 'Администрирование и поддержка серверов печати', 'Управление антивирусной защитой в корпоративной среде', 'Организация рабочих мест пользователей в крупной компании', 'Инфраструктурная поддержка в международной ИТ-компании'], 'gaps': ['Нет упоминания опыта работы с современными облачными технологиями (например, AWS, Azure, Google Cloud)', 'Отсутствует информация о навыках программирования или автоматизации (например, PowerShell, Python)', 'Нет упоминания о работе с современными инструментами DevOps (например, Docker, Kubernetes, CI/CD)'], 'recommendations': ['Указать опыт работы с облачными платформами, если имеется', 'Добавить информацию о навыках программирования или автоматизации процессов', 'Упомянуть опыт работы с современными инструментами DevOps, если применимо', 'Подчеркнуть достижения, связанные с оптимизацией ИТ-процессов и экономией ресурсов', 'Обновить резюме с учетом современных требований рынка труда'], 'personal_info': {}, 'experience_analysis': {}, 'skills_analysis': {}, 'overall_assessment': {}}	2025-08-30 23:44:02.814479+00	{}
BLOCK_EBA4C6CA	RESUME_912F63A4	education	Education	2003: Международный Университет, переводческое дело, переводчик-референт. 2023: Service Desk и процессы поддержки ИТ услуг (Центр компьютерного обучения Специалист при МГТУ им. Н.Э. Баумана). 2019: Linux. Уровень 1. Основы администрирования (Центр компьютерного обучения Специалист при МГТУ им. Н.Э. Баумана). 2017: Курс 10961: Автоматизация административных задач при помощи Windows PowerShell 3.0 (Центр компьютерного обучения Специалист при МГТУ им. Н.Э. Баумана). 2015: ITIL Foundation. IT Service Management (Центр компьютерного обучения Специалист при МГТУ им. Н.Э. Баумана). 2014: Курс Microsoft: Концепция Cloud OS: Windows 8 Enterprise для ИТ специалистов (Технологический Центр Microsoft). 2008: Курсы Microsoft: (M5047, M5049, M5050, M5051) Exchange Server 2007/Администратор почтовой системы (Центр компьютерного обучения Специалист при МГТУ им. Н.Э. Баумана). 2005: Курсы Microsoft: М2273: Управление и поддержка среды Microsoft Windows Server 2003 (Центр компьютерного обучения Специалист при МГТУ им. Н.Э. Баумана).	100.00	75.00	\N	\N	{'candidate_level': 'bachelor', 'required_level': 'bachelor', 'score': 100}	2025-08-30 23:44:02.814479+00	{}
BLOCK_D2FFED1F	RESUME_C19671C8	personal_info	Personal Info	Проживает: Москва.\nГражданство: Россия.\nЕсть разрешение на работу: Россия.\nНе готова к переезду, готова к редким командировкам.	50.00	80.00	\N	\N	\N	2025-08-30 23:46:10.981504+00	\N
BLOCK_B9B7F088	RESUME_C19671C8	education	Education	Высшее образование:\n- 2012: ГОУ ВПО Государственный университет управления, менеджмент организации, менеджер.\n- 2007: ГОУ Банковский колледж №1, банковское дело, специалист банковского дела.	100.00	75.00	\N	\N	{'candidate_level': 'bachelor', 'required_level': 'bachelor', 'score': 100}	2025-08-30 23:46:10.981504+00	{}
BLOCK_BFC409B3	RESUME_C19671C8	experience	Experience	- Автоматизация проверок для оценки риска мошенничества по кредитным заявкам.\n- Управление требованиями.\n- Взаимодействие с заинтересованными лицами.\n- Проектирование систем.\n- Моделирование бизнес-процессов и бизнес-правил.\n- Участие в поддержке системы на всех стадиях жизненного цикла.\n- Участие в создании пользовательского интерфейса.\n- Участие в решении инцидентов, тестировании, демонстрации нового функционала.\n- Участие в формировании бэклога команды.\n- Участие в оптимизации внутренних командных процессов.	0.00	85.00	\N	\N	{'relevant_years': '0', 'relevance_score': '0', 'key_achievements': [], 'relevant_projects': [], 'gaps': ['Отсутствие требований вакансии делает невозможным оценку релевантности опыта.'], 'recommendations': ['Предоставьте требования вакансии для корректного анализа.'], 'personal_info': {}, 'experience_analysis': {}, 'skills_analysis': {}, 'overall_assessment': {}}	2025-08-30 23:46:10.981504+00	{}
BLOCK_E326E94C	RESUME_C19671C8	skills	Skills	SQL, Работа с требованиями, Взаимодействие со стейкхолдерами, Декомпозиция задач, Коммуникативные навыки, User Story, Управление знаниями, Управление бэклогом, Приемочное тестирование.	50.00	50.00	\N	\N	No required skills specified	2025-08-30 23:46:10.981504+00	{}
BLOCK_167E5FC1	RESUME_54929C26	personal_info	Personal Info	Проживает: Москва, м. Крылатское Гражданство: Россия Не готов к переезду, готов к командировкам. Знание языков: Русский Родной, Английский B1 Средний. Имеется собственный автомобиль, права категории B.	50.00	80.00	\N	\N	\N	2025-08-30 23:46:42.334046+00	\N
BLOCK_D5F89635	RESUME_54929C26	skills	Skills	UX-исследования AS IS/TO BE mapping User Story Use case Анализ обратной связи Анализ бизнес-процессов Многозадачность Организаторские навыки Стратегическое мышление Управление ресурсами Управление бэклогом BPMN	50.00	50.00	\N	\N	No required skills specified	2025-08-30 23:46:42.334046+00	{}
BLOCK_DCF044DB	RESUME_54929C26	education	Education	Высшее образование: 2025 МГУ, Москва Бизнес-информатика, Бизнес-информатика; 2019 МГТУ им. Баумана Автоматизация. Повышение квалификации, курсы: 2025 Школа бизнес анализа (Пульс) Сбербанк, Бизнес аналитик	100.00	75.00	\N	\N	{'candidate_level': 'bachelor', 'required_level': 'bachelor', 'score': 100}	2025-08-30 23:46:42.334046+00	{}
BLOCK_3017C35A	RESUME_54929C26	experience	Experience	ПАО СБЕРБАНК Бизнес-аналитик Обязанности: - Выявлял потребности заказчика, моделировал бизнес-процессы, выполнял прототипирование пользовательского интерфейса, готовил Т3 для команды разработки - Проводил анализ, валидацию, документирование бизнес, функциональных, нефункциональных требований на изменение текущих и запуск новых технологических процессов Банка (Use case, User Story, CJM) - Декомпозировал бизнес-требования до формализованных задач командам разработки на изменение/внедрение IT систем - Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard - Занимался имплементацией self-service no code платформы на базе Camunda (BPMN 2.0), предназначенной для управления потоками данных в Кредитной машине Банка - Создавал и структурировал документацию в рамках команд, интегрировал задачи и проекты с соответствующими страницами (Confluence, Jira) - Проводил мероприятия связанные с тестированием разработанных решений, демонстрацией решений для заказчиков и сбор обратной связи - Проводил UX исследования и расписывал варианты улучшения клиентского опыта - Описывал Т3 для продуктовых дизайнеров и привлекал внешние ресурсы дизайна на проекты - Инициировал проведение CustDev для будущих пользователей платформы самообслуживания, что позволило улучшить пользовательский интерфейс панели управления - Описывал as is / to be, use case, user story - Проводил регулярную коммуникацию с командой разработчиков для оперативного решения возникающих вопросов и устранения несоответствий - Поддерживал актуальность документации по требованиям на протяжении всего проекта	85.00	85.00	\N	\N	{'relevant_years': '3-5 лет (предполагается, что опыт в ПАО СБЕРБАНК охватывает данный период)', 'relevance_score': 85, 'key_achievements': ['Имплементация self-service no code платформы на базе Camunda (BPMN 2.0)', 'Инициирование проведения CustDev для улучшения пользовательского интерфейса', 'Проведение UX исследований и улучшение клиентского опыта', 'Декомпозиция бизнес-требований до задач для IT-команд', 'Моделирование бизнес-процессов и прототипирование интерфейсов'], 'relevant_projects': ['Разработка и внедрение self-service no code платформы для управления потоками данных', 'Проекты, связанные с изменением и запуском новых технологических процессов Банка', 'UX исследования и улучшение клиентского опыта', 'Создание и поддержка документации в Confluence и Jira'], 'gaps': ['Отсутствие информации о конкретных результатах внедрения (например, количественные показатели улучшений)', 'Нет упоминания о знании специфических технологий или методологий, которые могут быть требуемы для вакансии (например, Agile, Scrum, SQL, API-интеграции, если они важны)', 'Не указаны детали о масштабах проектов (количество пользователей, объем данных и т.д.)'], 'recommendations': ['Уточнить количественные результаты работы (например, сокращение времени выполнения процессов, повышение удовлетворенности клиентов и т.д.)', 'Добавить информацию о масштабах проектов и их влиянии на бизнес', 'Указать владение дополнительными инструментами или технологиями, если они релевантны вакансии', 'Уточнить опыт работы с методологиями управления проектами (если применимо)'], 'personal_info': {}, 'experience_analysis': {}, 'skills_analysis': {}, 'overall_assessment': {}}	2025-08-30 23:46:42.334046+00	{}
BLOCK_A05D8DB2	RESUME_4213C3EF	experience	Experience	| Проживает: Москва, м. Крылатское Гражданство: Россия Не готов к переезду, готов к командировкам| Желаемая должность и зарплата| Аналитик Специализации:  Бизнес-аналитик Занятость: полная занятость, проектная работа График работы: полный день, гибкий график, удаленная работа Желательное время в пути до работы: не более часа|| Опыт работы 11 месяцев| Октябрь 2024  настоящее время 11 месяцев| |ПАО СБЕРБАНК Бизнес-аналитик Обязанности: -Выявлял потребности заказчика, моделировал бизнес-процессы, выполнял прототипирование пользовательского интерфейса, готовил Т3 для команды разработки -Проводил анализ, валидацию, документирование бизнес, функциональных, нефункциональных требований на изменение текущих и запуск новых технологических процессов Банка (Use case, User Story, CJM) - Декомпозировал бизнес-требования до формализованных задач командам разработки на изменение/внедрение IT систем -Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard -Занимался имплементацией self-service no code платформы на базе Camunda (BPMN 2.0), предназначенной для управления потоками данных в Кредитной машине Банка -Создавал и структурировал документацию в рамках команд, интегрировал задачи и проекты с соответсвующими страницами (Confluence, Jira) -Проводил мероприятия связанные с тестированием разработанных решений, демонстрацией решений для заказчиков и сбор обратной связи -Проводил UX исследования и расписывал варианты улучшения клиентского опыта -Описывал Т3 для продуктовых дизайнеров и привлекал внешние ресурсы дизайна на проекты -Инициировал проведение CustDev для будущих пользователей платформы самообслуживания, что позволило улучшить пользовательский интерфейс панели управления - Описывал as is / to be, use case, user story - Проводил регулярную коммуникацию с командой разработчиков для оперативного решения возникающих вопросов и устранения несоответствий - Поддерживал актуальность документации по требованиям на протяжении всего проекта| Образование| Высшее| 2025|МГУ, Москва Бизнес-информатика , Бизнес-информатика| 2019|МГТУ им. Баумана Автоматизация| Повышение квалификации, курсы| 2025|Школа бизнес анализа (Пульс) Сбербанк, Бизнес аналитик| Навыки| Знание языков|Русский  Родной Английский  B1  Средний| Навыки|UX-исследования AS IS/TO BE mapping User Story Use case Анализ обратной связи Анализ бизнес-процессов Многозадачность Организаторские навыки Стратегическое мышление Английский язык Управление ресурсами Управление бэклогом BPMN| Опыт вождения| Имеется собственный автомобиль Права категории B| Дополнительная информация| Обо мне||	50.00	80.00	\N	\N	\N	2025-09-03 18:45:52.666779+00	\N
\.


--
-- Data for Name: resume_skills; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.resume_skills (id, resume_id, skill_name, skill_category, experience_level, years_experience, confidence_score, extracted_from, created_at) FROM stdin;
SKILL_1324F79F	RESUME_912F63A4	Active Directory	tools	expert	\N	90.00	работа с MSActiveDirectory,DNS,DHCP.	2025-08-30 23:44:35.859492+00
SKILL_159EA75D	RESUME_912F63A4	Windows Server	tools	expert	\N	90.00	сопровождение и поддержка серверов на базе ОС Windows Server/Windows Server 2008	2025-08-30 23:44:35.859492+00
SKILL_59B634C7	RESUME_912F63A4	DNS	tools	expert	\N	85.00	работа с MSActiveDirectory,DNS,DHCP.	2025-08-30 23:44:35.859492+00
SKILL_4F2883C2	RESUME_912F63A4	DHCP	tools	expert	\N	85.00	работа с MSActiveDirectory,DNS,DHCP.	2025-08-30 23:44:35.859492+00
SKILL_1B1239E8	RESUME_912F63A4	Kaspersky Security Center	tools	intermediate	\N	80.00	управление антивирусной защитой на базе Kaspersky Security Center	2025-08-30 23:44:35.859492+00
SKILL_5C4BC753	RESUME_912F63A4	Windows OS	tools	expert	\N	90.00	подготовка рабочих станций на Windows, Linux, Mac OS.	2025-08-30 23:44:35.859492+00
SKILL_B9479BF6	RESUME_912F63A4	Linux OS	tools	intermediate	\N	90.00	подготовка рабочих станций на Windows, Linux, Mac OS.	2025-08-30 23:44:35.859492+00
SKILL_89DAFECC	RESUME_912F63A4	Mac OS	tools	intermediate	\N	85.00	подготовка рабочих станций на Windows, Linux, Mac OS.	2025-08-30 23:44:35.859492+00
SKILL_441A098E	RESUME_912F63A4	VBScript	programming	intermediate	\N	80.00	написание скриптов на VBScript	2025-08-30 23:44:35.859492+00
SKILL_D413E503	RESUME_912F63A4	PowerShell	programming	intermediate	\N	85.00	Курс 10961: Автоматизация административных задач при помощи Windows PowerShell 3.0	2025-08-30 23:44:35.859492+00
SKILL_5FBEAAB0	RESUME_912F63A4	1C Itilium	tools	intermediate	\N	75.00	тестирование программ Service Desk по управлению обращениями пользователей 1C Itilium.	2025-08-30 23:44:35.859492+00
SKILL_522D010F	RESUME_912F63A4	Service Desk	tools	intermediate	\N	80.00	тестирование программ Service Desk по управлению обращениями пользователей	2025-08-30 23:44:35.859492+00
SKILL_0F7353B6	RESUME_912F63A4	Lotus Notes	tools	beginner	\N	70.00	опыт в поддержке почтового клиента Lotus Notes в корпоративной среде.	2025-08-30 23:44:35.859492+00
SKILL_9BA9EC4B	RESUME_912F63A4	Windows Deployment Services (WDS)	tools	intermediate	\N	80.00	внедрение MS Windows Deployment Server для клонирования образов по сети	2025-08-30 23:44:35.859492+00
SKILL_35E231FD	RESUME_912F63A4	HP Jet Admin	tools	intermediate	\N	75.00	внедрение мониторинга печатающих устройств (свыше 80 устройств) на базе HP Jet Admin	2025-08-30 23:44:35.859492+00
SKILL_00C5D872	RESUME_912F63A4	Zebra Printers	tools	beginner	\N	70.00	мониторинг печатающих устройств... термо-принтеров Zebra	2025-08-30 23:44:35.859492+00
SKILL_B8C36286	RESUME_912F63A4	Datamax Printers	tools	beginner	\N	70.00	мониторинг печатающих устройств... термо-принтеров Datamax	2025-08-30 23:44:35.859492+00
SKILL_896B4A80	RESUME_912F63A4	ITIL	methodologies	intermediate	\N	85.00	ITIL Foundation. IT Service Management.	2025-08-30 23:44:35.859492+00
SKILL_43971D5A	RESUME_912F63A4	GPO (Group Policy Objects)	tools	intermediate	\N	80.00	GPO для подключения сетевых принтеров согласно членству пользователя в группах безопасности.	2025-08-30 23:44:35.859492+00
SKILL_3159530C	RESUME_912F63A4	Microsoft Exchange Server	tools	intermediate	\N	80.00	курсы Microsoft: (M5047, M5049, M5050, M5051) Exchange Server 2007/Администратор почтовой системы	2025-08-30 23:44:35.859492+00
SKILL_054811AF	RESUME_912F63A4	Radmin	tools	beginner	\N	70.00	средства удаленного администрирования - Radmin и др.	2025-08-30 23:44:35.859492+00
SKILL_09E91360	RESUME_912F63A4	Atlassian Jira Service Desk	tools	beginner	\N	70.00	Навыки: Atlassian Jira Service Desk	2025-08-30 23:44:35.859492+00
SKILL_B8A3B0EC	RESUME_912F63A4	HP Printers	tools	intermediate	\N	80.00	сопровождение широкой линейки высокопроизводительных принтеров HP	2025-08-30 23:44:35.859492+00
SKILL_E205BDA6	RESUME_D0A2DD98	SQL	programming	intermediate	\N	80.00	Навыки SQL	2025-08-30 23:44:46.525666+00
SKILL_E760AAC2	RESUME_D0A2DD98	Python	programming	intermediate	\N	85.00	написание скриптов bash/python	2025-08-30 23:44:46.525666+00
SKILL_D5F603C8	RESUME_D0A2DD98	PHP	programming	beginner	\N	70.00	Навыки PHP	2025-08-30 23:44:46.525666+00
SKILL_46166C18	RESUME_D0A2DD98	Bash	programming	intermediate	\N	85.00	написание скриптов bash/python	2025-08-30 23:44:46.525666+00
SKILL_4D9FE0BD	RESUME_D0A2DD98	Прокладка кабелей	tools	expert	\N	90.00	Прокладка кроссовых трасс, кабель менеджмент	2025-08-30 23:44:46.525666+00
SKILL_DB1BCD41	RESUME_D0A2DD98	Техническое обслуживание	tools	expert	\N	90.00	Сборка, техобслуживание, проверка серверного оборудования	2025-08-30 23:44:46.525666+00
SKILL_47972A19	RESUME_D0A2DD98	Сетевые технологии	methodologies	intermediate	\N	80.00	Настройка конфигурации сетевого оборудования	2025-08-30 23:44:46.525666+00
SKILL_0D3EAD26	RESUME_D0A2DD98	OSI	methodologies	beginner	\N	70.00	Навыки OSI	2025-08-30 23:44:46.525666+00
SKILL_E40DC7B3	RESUME_D0A2DD98	MikroTik	tools	intermediate	\N	80.00	Навыки MikroTik	2025-08-30 23:44:46.525666+00
SKILL_D4E5A80B	RESUME_D0A2DD98	Cisco	tools	intermediate	\N	85.00	Навыки Cisco	2025-08-30 23:44:46.525666+00
SKILL_65CE6EBF	RESUME_D0A2DD98	SSH	tools	intermediate	\N	80.00	Навыки SSH	2025-08-30 23:44:46.525666+00
SKILL_D38FCC0C	RESUME_D0A2DD98	Ubuntu	tools	intermediate	\N	85.00	Навыки Ubuntu	2025-08-30 23:44:46.525666+00
SKILL_9260F517	RESUME_D0A2DD98	Сборка ПК	tools	expert	\N	90.00	Сборка оборудования, замена и установка комплектующих	2025-08-30 23:44:46.525666+00
SKILL_92FC1664	RESUME_D0A2DD98	Сборка серверов	tools	expert	\N	90.00	Сборка оборудования, замена и установка комплектующих	2025-08-30 23:44:46.525666+00
SKILL_EDA99737	RESUME_D0A2DD98	Windows Server	tools	intermediate	\N	80.00	Навыки Windows Server	2025-08-30 23:44:46.525666+00
SKILL_A37B7FA6	RESUME_D0A2DD98	Настройка ПК	tools	intermediate	\N	85.00	Настройка сетевого и серверного оборудования, включая роутеры, принтеры, пк	2025-08-30 23:44:46.525666+00
SKILL_C52B5527	RESUME_D0A2DD98	Настройка ПО	tools	intermediate	\N	85.00	Настройка и установка дистрибутивов	2025-08-30 23:44:46.525666+00
SKILL_785B6F3A	RESUME_D0A2DD98	Настройка сетевых подключений	tools	intermediate	\N	85.00	Настройка конфигурации сетевого оборудования	2025-08-30 23:44:46.525666+00
SKILL_80F70723	RESUME_D0A2DD98	Информационные технологии	methodologies	beginner	\N	70.00	Навыки Информационные технологии	2025-08-30 23:44:46.525666+00
SKILL_EB5E0B99	RESUME_D0A2DD98	Администрирование	methodologies	intermediate	\N	80.00	В дальнейшем - Администратор АО	2025-08-30 23:44:46.525666+00
SKILL_B79DDB9C	RESUME_D0A2DD98	Техническая поддержка	methodologies	expert	\N	90.00	Обработка обращений клиентов, настройка оборудования	2025-08-30 23:44:46.525666+00
SKILL_134DFC25	RESUME_C19671C8	SQL	databases	expert	\N	95.00	Навыки: SQL	2025-08-30 23:46:20.054063+00
SKILL_84AC0A46	RESUME_C19671C8	Работа с требованиями	methodologies	expert	\N	90.00	Навыки: Работа с требованиями	2025-08-30 23:46:20.054063+00
SKILL_A1658477	RESUME_C19671C8	Взаимодействие со стейкхолдерами	methodologies	expert	\N	90.00	Навыки: Взаимодействие со стейкхолдерами	2025-08-30 23:46:20.054063+00
SKILL_FCA2FBF2	RESUME_C19671C8	Декомпозиция задач	methodologies	expert	\N	85.00	Навыки: Декомпозиция задач	2025-08-30 23:46:20.054063+00
SKILL_60416403	RESUME_C19671C8	User Story	methodologies	intermediate	\N	85.00	Навыки: User Story	2025-08-30 23:46:20.054063+00
SKILL_233C9CE6	RESUME_C19671C8	Управление знаниями	methodologies	expert	\N	90.00	Навыки: Управление знаниями	2025-08-30 23:46:20.054063+00
SKILL_84F0C254	RESUME_C19671C8	Управление бэклогом	methodologies	intermediate	\N	85.00	Навыки: Управление бэклогом	2025-08-30 23:46:20.054063+00
SKILL_42C2CA10	RESUME_C19671C8	Приемочное тестирование	methodologies	intermediate	\N	85.00	Навыки: Приемочное тестирование	2025-08-30 23:46:20.054063+00
SKILL_F35B3055	RESUME_C19671C8	Моделирование бизнес-процессов	methodologies	expert	\N	90.00	Проектирование систем, моделирование бизнес-процессов и бизнес-правил	2025-08-30 23:46:20.054063+00
SKILL_96F268BC	RESUME_C19671C8	Проектирование систем	methodologies	expert	\N	90.00	Проектирование систем, моделирование бизнес-процессов и бизнес-правил	2025-08-30 23:46:20.054063+00
SKILL_7E069594	RESUME_54929C26	Miro	tools	intermediate	\N	90.00	Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard	2025-08-30 23:46:55.494097+00
SKILL_15EF117F	RESUME_54929C26	draw.io	tools	intermediate	\N	90.00	Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard	2025-08-30 23:46:55.494097+00
SKILL_8FA0D151	RESUME_54929C26	whiteboard	tools	intermediate	\N	80.00	Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard	2025-08-30 23:46:55.494097+00
SKILL_F66679FA	RESUME_54929C26	Camunda	tools	intermediate	\N	90.00	Занимался имплементацией self-service no code платформы на базе Camunda (BPMN 2.0)	2025-08-30 23:46:55.494097+00
SKILL_A9BBBD06	RESUME_54929C26	BPMN 2.0	methodologies	intermediate	\N	90.00	Занимался имплементацией self-service no code платформы на базе Camunda (BPMN 2.0)	2025-08-30 23:46:55.494097+00
SKILL_4072537D	RESUME_54929C26	Confluence	tools	intermediate	\N	90.00	Создавал и структурировал документацию в рамках команд, интегрировал задачи и проекты с соответсвующими страницами (Confluence, Jira)	2025-08-30 23:46:55.494097+00
SKILL_72530986	RESUME_54929C26	Jira	tools	intermediate	\N	90.00	Создавал и структурировал документацию в рамках команд, интегрировал задачи и проекты с соответсвующими страницами (Confluence, Jira)	2025-08-30 23:46:55.494097+00
SKILL_2138EA1F	RESUME_54929C26	UX-исследования	methodologies	expert	\N	95.00	Проводил UX исследования и расписывал варианты улучшения клиентского опыта	2025-08-30 23:46:55.494097+00
SKILL_49579C23	RESUME_54929C26	AS IS/TO BE mapping	methodologies	expert	\N	95.00	Описывал as is / to be, use case, user story	2025-08-30 23:46:55.494097+00
SKILL_34879CF6	RESUME_54929C26	Use case	methodologies	expert	\N	95.00	Описывал as is / to be, use case, user story	2025-08-30 23:46:55.494097+00
SKILL_5C4C4C0C	RESUME_54929C26	User Story	methodologies	expert	\N	95.00	Описывал as is / to be, use case, user story	2025-08-30 23:46:55.494097+00
SKILL_14E22F02	RESUME_54929C26	CustDev	methodologies	intermediate	\N	80.00	Инициировал проведение CustDev для будущих пользователей платформы самообслуживания	2025-08-30 23:46:55.494097+00
SKILL_216B0B06	RESUME_54929C26	Анализ бизнес-процессов	methodologies	expert	\N	95.00	Выявлял потребности заказчика, моделировал бизнес-процессы	2025-08-30 23:46:55.494097+00
SKILL_60CCEE23	RESUME_4213C3EF	Miro	tools	intermediate	\N	90.00	Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard	2025-09-03 18:46:03.550397+00
SKILL_7636F47C	RESUME_4213C3EF	draw.io	tools	intermediate	\N	90.00	Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard	2025-09-03 18:46:03.550397+00
SKILL_59AC9AB7	RESUME_4213C3EF	whiteboard	tools	intermediate	\N	80.00	Работал со следующими инструментами прототипирования: Miro, draw.io и whiteboard	2025-09-03 18:46:03.550397+00
SKILL_BABE3C11	RESUME_4213C3EF	Camunda	tools	intermediate	\N	90.00	Занимался имплементацией self-service no code платформы на базе Camunda (BPMN 2.0)	2025-09-03 18:46:03.550397+00
SKILL_BF5A9F27	RESUME_4213C3EF	BPMN 2.0	methodologies	intermediate	\N	90.00	Занимался имплементацией self-service no code платформы на базе Camunda (BPMN 2.0)	2025-09-03 18:46:03.550397+00
SKILL_848888EF	RESUME_4213C3EF	Confluence	tools	intermediate	\N	90.00	Создавал и структурировал документацию в рамках команд, интегрировал задачи и проекты с соответсвующими страницами (Confluence, Jira)	2025-09-03 18:46:03.550397+00
SKILL_0CBC93BC	RESUME_4213C3EF	Jira	tools	intermediate	\N	90.00	Создавал и структурировал документацию в рамках команд, интегрировал задачи и проекты с соответсвующими страницами (Confluence, Jira)	2025-09-03 18:46:03.550397+00
SKILL_54B8CFCE	RESUME_4213C3EF	UX-исследования	methodologies	intermediate	\N	85.00	Проводил UX исследования и расписывал варианты улучшения клиентского опыта	2025-09-03 18:46:03.550397+00
SKILL_1778515B	RESUME_4213C3EF	CustDev	methodologies	intermediate	\N	80.00	Инициировал проведение CustDev для будущих пользователей платформы самообслуживания	2025-09-03 18:46:03.550397+00
SKILL_5C0FAC8F	RESUME_4213C3EF	AS IS/TO BE mapping	methodologies	intermediate	\N	90.00	Описывал as is / to be, use case, user story	2025-09-03 18:46:03.550397+00
SKILL_593836EE	RESUME_4213C3EF	Use case	methodologies	intermediate	\N	90.00	Описывал as is / to be, use case, user story	2025-09-03 18:46:03.550397+00
SKILL_50201FEF	RESUME_4213C3EF	User Story	methodologies	intermediate	\N	90.00	Описывал as is / to be, use case, user story	2025-09-03 18:46:03.550397+00
SKILL_34430EEB	RESUME_4213C3EF	Анализ бизнес-процессов	methodologies	intermediate	\N	85.00	Проводил анализ, валидацию, документирование бизнес, функциональных, нефункциональных требований	2025-09-03 18:46:03.550397+00
SKILL_5DDCF882	RESUME_4213C3EF	Прототипирование	methodologies	intermediate	\N	85.00	Выявлял потребности заказчика, моделировал бизнес-процессы, выполнял прототипирование пользовательского интерфейса	2025-09-03 18:46:03.550397+00
\.


--
-- Data for Name: resumes; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.resumes (id, vacancy_id, vacancy_code, filename, original_filename, file_size, file_type, upload_date, status, total_score, confidence_score, processing_errors, created_at, updated_at) FROM stdin;
RESUME_912F63A4	SWE_BACK_001	\N	af6b15b9875945998726338476656611.docx	Образец резюме 1 Ведущий специалист ИТ.docx	19537	docx	2025-08-30 23:44:02.779029+00	analyzed	67.00	64.00	\N	2025-08-30 23:44:02.779029+00	2025-08-30 23:44:46.535308+00
RESUME_D0A2DD98	SWE_BACK_001	\N	cc1e646d92794fc59d4e6c8c8eaa932f.docx	Образец резюме 2 Ведущий специалист ИТ.docx	14607	docx	2025-08-30 23:44:02.760571+00	analyzed	69.00	64.00	\N	2025-08-30 23:44:02.760571+00	2025-08-30 23:44:52.117479+00
RESUME_C19671C8	af625a8d-1f69-4aea-9d2f-2d5b504ef215	\N	1e0f7250b6cc4e8e9bc7d0145157adf3.rtf	Образец резюме 1 Бизнес аналитик.rtf	231568	rtf	2025-08-30 23:46:09.016406+00	analyzed	35.00	64.00	\N	2025-08-30 23:46:09.016406+00	2025-08-30 23:46:20.063083+00
RESUME_54929C26	af625a8d-1f69-4aea-9d2f-2d5b504ef215	\N	7bce34f6e5834d8cb2f3cbfe24d6e254.rtf	Образец резюме 2 Бизнес аналитик.rtf	139402	rtf	2025-08-30 23:46:41.135761+00	analyzed	69.00	64.00	\N	2025-08-30 23:46:41.135761+00	2025-08-30 23:47:02.235348+00
RESUME_4213C3EF	\N	\N	1a6208b7a5114ee2bcfaa5bbb9ef4af6.rtf	Образец резюме 2 Бизнес аналитик.rtf	139402	rtf	2025-09-03 18:45:48.900123+00	analyzed	0.00	28.00	\N	2025-09-03 18:45:48.900123+00	2025-09-03 18:46:03.550397+00
\.


--
-- Data for Name: scenario_criteria_mappings; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.scenario_criteria_mappings (id, scenario_id, criterion_id, weight, is_mandatory, min_score, created_at, updated_at) FROM stdin;
MAPPING_40F3D93B	SCENARIO_844827A6	DC_051833A4	1	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_3A74EA2B	SCENARIO_844827A6	DC_1B573816	0.8	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_EB398817	SCENARIO_844827A6	DC_F72F33A2	0.8	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_0C4832C1	SCENARIO_844827A6	DC_30395874	0.7	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_CE57B2A1	SCENARIO_844827A6	DC_5321F05A	1	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_506F066C	SCENARIO_844827A6	DC_FCF31438	0.8	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_CE6F682F	SCENARIO_844827A6	DC_64965B36	0.7	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_6BA58528	SCENARIO_844827A6	DC_8923BCE6	0.6	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_270BF57C	SCENARIO_844827A6	DC_46F7A970	0.9	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_34DAF43F	SCENARIO_844827A6	DC_B062FA74	0.8	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_63416BB5	SCENARIO_844827A6	DC_6EEDB5D4	0.7	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_17D8CAD2	SCENARIO_844827A6	DC_7160BAAA	0.8	t	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_ACB2F5D1	SCENARIO_844827A6	DC_3F439185	0.6	f	\N	2025-08-31 00:39:33.86326+00	2025-08-31 00:39:33.86326+00
MAPPING_27E78D60	SCENARIO_A9DB7161	DC_FB042B8A	0.8	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_E4AE191C	SCENARIO_A9DB7161	DC_4BFEEDA7	0.9	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_59E3C3FA	SCENARIO_A9DB7161	DC_7A5C3E4F	0.7	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_6982F331	SCENARIO_A9DB7161	DC_CE68EF45	1	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_EF72696E	SCENARIO_A9DB7161	DC_C052EC21	0.7	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_44964245	SCENARIO_A9DB7161	DC_CB9E7CD7	0.6	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_A466DEAD	SCENARIO_A9DB7161	DC_8D4252B7	0.6	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_95833118	SCENARIO_A9DB7161	DC_67980DFD	0.7	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_0DBD0E68	SCENARIO_A9DB7161	DC_A9D73CEA	0.7	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_F58F5545	SCENARIO_A9DB7161	DC_A8E65A22	0.8	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_4B1C963C	SCENARIO_A9DB7161	DC_6D876D08	0.9	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_E3228494	SCENARIO_A9DB7161	DC_A56DB3CA	0.8	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_0E450452	SCENARIO_A9DB7161	DC_66B82996	0.7	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_1EBFFAA4	SCENARIO_A9DB7161	DC_B142F68D	0.8	f	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_B3AE1B59	SCENARIO_A9DB7161	DC_5EE15513	1	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_844692B8	SCENARIO_A9DB7161	DC_52B1C668	0.9	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_E5E1D1AC	SCENARIO_A9DB7161	DC_3BB9E9DC	1	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_5F40C8DB	SCENARIO_A9DB7161	DC_F8D29743	0.8	t	\N	2025-08-31 01:04:46.903732+00	2025-08-31 01:04:46.903732+00
MAPPING_EB1CFB32	SCENARIO_A0EE5ADE	DC_FAAED486	1	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_332F03C2	SCENARIO_A0EE5ADE	DC_95157690	0.8	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_A412E16D	SCENARIO_A0EE5ADE	DC_5AD50C48	0.8	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_E0836CBD	SCENARIO_A0EE5ADE	DC_6C455EE2	0.7	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_0BCB1447	SCENARIO_A0EE5ADE	DC_BB650A26	1	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_724D2B8F	SCENARIO_A0EE5ADE	DC_C9C63AE0	0.8	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_C43C1B7A	SCENARIO_A0EE5ADE	DC_F5029AE1	0.7	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_29381283	SCENARIO_A0EE5ADE	DC_596432B8	0.6	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_AA26D06C	SCENARIO_A0EE5ADE	DC_2E87BCAC	0.9	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_1B10EF09	SCENARIO_A0EE5ADE	DC_8EB3A78F	0.8	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_64B8B920	SCENARIO_A0EE5ADE	DC_933233B6	0.7	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_52334B20	SCENARIO_A0EE5ADE	DC_BC89B741	0.8	t	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
MAPPING_D9F0A3D7	SCENARIO_A0EE5ADE	DC_ABE7ED7B	0.6	f	\N	2025-08-31 01:21:36.189137+00	2025-08-31 01:21:36.189137+00
\.


--
-- Data for Name: scenario_nodes; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.scenario_nodes (id, scenario_id, question_id, node_type, position_x, position_y, node_config, created_at, updated_at) FROM stdin;
start	SCENARIO_844827A6	\N	start	100	100	{"label": "\\u041d\\u0430\\u0447\\u0430\\u043b\\u043e \\u0438\\u043d\\u0442\\u0435\\u0440\\u0432\\u044c\\u044e", "weight": 1.0, "must_have": false}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_1	SCENARIO_844827A6	\N	question	300	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u044586", "weight": 1.0, "must_have": true, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u044586"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_2	SCENARIO_844827A6	\N	question	500	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0445 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u0445 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c", "weight": 0.8, "must_have": true, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0445 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u0445 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_3	SCENARIO_844827A6	\N	question	700	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0435\\u0442\\u0435\\u0439 \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0438 \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "weight": 0.8, "must_have": true, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0435\\u0442\\u0435\\u0439 \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0438 \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_4	SCENARIO_844827A6	\N	question	900	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0446\\u0435\\u043d\\u0442\\u0440\\u043e\\u0432 \\u043e\\u0431\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "weight": 0.7, "must_have": true, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0446\\u0435\\u043d\\u0442\\u0440\\u043e\\u0432 \\u043e\\u0431\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_5	SCENARIO_844827A6	\N	question	1100	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u043f\\u0435\\u0440\\u0432\\u0438\\u0447\\u043d\\u0430\\u044f \\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u044586", "weight": 1.0, "must_have": true, "target_skills": ["\\u043f\\u0435\\u0440\\u0432\\u0438\\u0447\\u043d\\u0430\\u044f \\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u044586"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_6	SCENARIO_844827A6	\N	question	1300	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Excel", "weight": 0.8, "must_have": true, "target_skills": ["\\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Excel"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_7	SCENARIO_844827A6	\N	question	1500	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Word", "weight": 0.7, "must_have": true, "target_skills": ["\\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Word"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
question_8	SCENARIO_844827A6	\N	question	1700	100	{"label": "\\u0412\\u043e\\u043f\\u0440\\u043e\\u0441 \\u043f\\u043e \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Visio", "weight": 0.6, "must_have": true, "target_skills": ["\\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Visio"]}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
end	SCENARIO_844827A6	\N	end	2900	100	{"label": "\\u0417\\u0430\\u0432\\u0435\\u0440\\u0448\\u0435\\u043d\\u0438\\u0435 \\u0438\\u043d\\u0442\\u0435\\u0440\\u0432\\u044c\\u044e", "weight": 1.0, "must_have": false}	2025-08-31 00:39:33.847891+00	2025-08-31 00:39:33.847891+00
SCENARIO_917B6C27_start	SCENARIO_A9DB7161	\N	start	100	100	{"label": "\\u041d\\u0430\\u0447\\u0430\\u043b\\u043e \\u0438\\u043d\\u0442\\u0435\\u0440\\u0432\\u044c\\u044e"}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_node_1	SCENARIO_A9DB7161	\N	question	300	100	{"label": "\\u041f\\u043e\\u0434\\u0433\\u043e\\u0442\\u043e\\u0432\\u043a\\u0430 \\u0431\\u0438\\u0437\\u043d\\u0435\\u0441-\\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439", "weight": 1.0, "must_have": true, "target_skills": ["\\u041f\\u043e\\u0434\\u0433\\u043e\\u0442\\u043e\\u0432\\u043a\\u0430 \\u0431\\u0438\\u0437\\u043d\\u0435\\u0441-\\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439", "\\u0410\\u043d\\u0430\\u043b\\u0438\\u0437 \\u0438 \\u0444\\u043e\\u0440\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439"]}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_node_2	SCENARIO_A9DB7161	\N	question	300	200	{"label": "\\u0424\\u043e\\u0440\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439", "weight": 1.0, "must_have": true, "target_skills": ["\\u0410\\u043d\\u0430\\u043b\\u0438\\u0437 \\u0438 \\u0444\\u043e\\u0440\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439"]}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_node_3	SCENARIO_A9DB7161	\N	question	300	300	{"label": "\\u0423\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0430\\u043d\\u0442\\u0438\\u0444\\u0440\\u043e\\u0434-\\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430\\u043c\\u0438", "weight": 1.0, "must_have": true, "target_skills": ["\\u0423\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u043e\\u0439 \\u043f\\u0440\\u043e\\u0442\\u0438\\u0432\\u043e\\u0434\\u0435\\u0439\\u0441\\u0442\\u0432\\u0438\\u044f \\u043c\\u043e\\u0448\\u0435\\u043d\\u043d\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u0443"]}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_node_4	SCENARIO_A9DB7161	\N	question	300	400	{"label": "\\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0430 \\u0442\\u0435\\u0441\\u0442-\\u043a\\u0435\\u0439\\u0441\\u043e\\u0432", "weight": 0.8, "must_have": false, "target_skills": ["\\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0430 \\u0442\\u0435\\u0441\\u0442-\\u043a\\u0435\\u0439\\u0441\\u043e\\u0432"]}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_node_5	SCENARIO_A9DB7161	\N	question	500	100	{"label": "\\u0418\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442\\u044b Microsoft Office", "weight": 0.8, "must_have": true, "target_skills": ["Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint"]}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_node_6	SCENARIO_A9DB7161	\N	question	500	200	{"label": "\\u041a\\u043e\\u0440\\u043f\\u043e\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u044b\\u0435 \\u043a\\u0430\\u0440\\u0442\\u044b", "weight": 0.6, "must_have": false, "target_skills": ["\\u041e\\u043f\\u044b\\u0442 \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u043a\\u043e\\u0440\\u043f\\u043e\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u044b\\u043c\\u0438 \\u043a\\u0430\\u0440\\u0442\\u0430\\u043c\\u0438"]}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_917B6C27_end	SCENARIO_A9DB7161	\N	end	700	300	{"label": "\\u0417\\u0430\\u0432\\u0435\\u0440\\u0448\\u0435\\u043d\\u0438\\u0435 \\u0438\\u043d\\u0442\\u0435\\u0440\\u0432\\u044c\\u044e"}	2025-08-31 01:04:46.891014+00	2025-08-31 01:04:46.891014+00
SCENARIO_85FE7B54_start	SCENARIO_A0EE5ADE	\N	start	100	100	{"label": "\\u041d\\u0430\\u0447\\u0430\\u043b\\u043e \\u0438\\u043d\\u0442\\u0435\\u0440\\u0432\\u044c\\u044e"}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_node_1	SCENARIO_A0EE5ADE	\N	question	300	100	{"label": "\\u0421\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0435 \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 x86", "weight": 1.0, "must_have": true, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u044586"]}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_node_2	SCENARIO_A0EE5ADE	\N	question	300	200	{"label": "\\u0421\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0435 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b", "weight": 0.8, "must_have": false, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0445 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u0445 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c"]}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_node_3	SCENARIO_A0EE5ADE	\N	question	300	300	{"label": "\\u0421\\u0435\\u0442\\u0438 \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0438 \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "weight": 0.8, "must_have": false, "target_skills": ["\\u0437\\u043d\\u0430\\u043d\\u0438\\u0435 \\u0441\\u0435\\u0442\\u0435\\u0439 \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0438 \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_node_4	SCENARIO_A0EE5ADE	\N	question	500	100	{"label": "\\u0414\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f", "weight": 1.0, "must_have": true, "target_skills": ["\\u043f\\u0435\\u0440\\u0432\\u0438\\u0447\\u043d\\u0430\\u044f \\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u044586"]}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_node_5	SCENARIO_A0EE5ADE	\N	question	500	200	{"label": "\\u0420\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Excel", "weight": 0.8, "must_have": false, "target_skills": ["\\u0440\\u0430\\u0431\\u043e\\u0442\\u0430 \\u0441 Excel"]}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_node_6	SCENARIO_A0EE5ADE	\N	question	500	300	{"label": "\\u041c\\u044f\\u0433\\u043a\\u0438\\u0435 \\u043d\\u0430\\u0432\\u044b\\u043a\\u0438", "weight": 0.9, "must_have": true, "target_skills": ["\\u043e\\u0442\\u0432\\u0435\\u0442\\u0441\\u0442\\u0432\\u0435\\u043d\\u043d\\u043e\\u0441\\u0442\\u044c", "\\u0430\\u043a\\u043a\\u0443\\u0440\\u0430\\u0442\\u043d\\u043e\\u0441\\u0442\\u044c \\u0432 \\u0440\\u0430\\u0431\\u043e\\u0442\\u0435", "\\u0438\\u0441\\u043f\\u043e\\u043b\\u043d\\u0438\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u044c"]}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
SCENARIO_85FE7B54_end	SCENARIO_A0EE5ADE	\N	end	700	200	{"label": "\\u041a\\u043e\\u043d\\u0435\\u0446 \\u0438\\u043d\\u0442\\u0435\\u0440\\u0432\\u044c\\u044e"}	2025-08-31 01:21:36.16766+00	2025-08-31 01:21:36.16766+00
\.


--
-- Data for Name: scenario_transitions; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.scenario_transitions (id, scenario_id, from_node_id, to_node_id, condition_type, condition_value, priority, transition_label, created_at, updated_at) FROM stdin;
TRANS_325034B4	SCENARIO_844827A6	start	question_1	always	{}	1	Переход 1	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_C958A486	SCENARIO_844827A6	question_1	question_2	always	{}	1	Переход 2	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_E3B22F4A	SCENARIO_844827A6	question_2	question_3	always	{}	1	Переход 3	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_73EF574A	SCENARIO_844827A6	question_3	question_4	always	{}	1	Переход 4	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_54937420	SCENARIO_844827A6	question_4	question_5	always	{}	1	Переход 5	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_0488380A	SCENARIO_844827A6	question_5	question_6	always	{}	1	Переход 6	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_1012BFD2	SCENARIO_844827A6	question_6	question_7	always	{}	1	Переход 7	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_75A98870	SCENARIO_844827A6	question_7	question_8	always	{}	1	Переход 8	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANS_0A672644	SCENARIO_844827A6	question_8	end	always	{}	1	Переход 9	2025-08-31 00:39:33.85581+00	2025-08-31 00:39:33.85581+00
TRANSITION_BD5A52AD	SCENARIO_A9DB7161	SCENARIO_917B6C27_start	SCENARIO_917B6C27_node_1	always	\N	1	Начать интервью	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_58CEB986	SCENARIO_A9DB7161	SCENARIO_917B6C27_node_1	SCENARIO_917B6C27_node_2	score_threshold	{"min_score": 0.7, "criterion": "overall_score"}	1	Переход к следующему вопросу (порог: 0.7)	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_BC3176F4	SCENARIO_A9DB7161	SCENARIO_917B6C27_node_2	SCENARIO_917B6C27_node_3	score_threshold	{"min_score": 0.7, "criterion": "overall_score"}	1	Переход к следующему вопросу (порог: 0.7)	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_B9293504	SCENARIO_A9DB7161	SCENARIO_917B6C27_node_3	SCENARIO_917B6C27_node_4	score_threshold	{"min_score": 0.7, "criterion": "overall_score"}	1	Переход к следующему вопросу (порог: 0.7)	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_86C514D6	SCENARIO_A9DB7161	SCENARIO_917B6C27_node_4	SCENARIO_917B6C27_node_5	always	\N	1	Переход к следующему вопросу	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_476B25F3	SCENARIO_A9DB7161	SCENARIO_917B6C27_node_5	SCENARIO_917B6C27_node_6	score_threshold	{"min_score": 0.7, "criterion": "overall_score"}	1	Переход к следующему вопросу (порог: 0.7)	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_7B650021	SCENARIO_A9DB7161	SCENARIO_917B6C27_node_6	SCENARIO_917B6C27_end	always	\N	1	Завершить интервью	2025-08-31 02:48:22.43085+00	2025-08-31 02:48:22.43085+00
TRANSITION_F1F2EEC8	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_start	SCENARIO_85FE7B54_node_1	always	\N	1	Начать интервью	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
TRANSITION_3492C522	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_node_1	SCENARIO_85FE7B54_node_2	score_threshold	{"min_score": 0.7, "criterion": "overall_score"}	1	Переход к следующему вопросу (порог: 0.7)	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
TRANSITION_5F79046E	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_node_2	SCENARIO_85FE7B54_node_3	always	\N	1	Переход к следующему вопросу	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
TRANSITION_3E3C8653	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_node_3	SCENARIO_85FE7B54_node_4	always	\N	1	Переход к следующему вопросу	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
TRANSITION_06B3CC4D	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_node_4	SCENARIO_85FE7B54_node_5	score_threshold	{"min_score": 0.7, "criterion": "overall_score"}	1	Переход к следующему вопросу (порог: 0.7)	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
TRANSITION_BCAB9B29	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_node_5	SCENARIO_85FE7B54_node_6	always	\N	1	Переход к следующему вопросу	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
TRANSITION_61BCC7F6	SCENARIO_A0EE5ADE	SCENARIO_85FE7B54_node_6	SCENARIO_85FE7B54_end	always	\N	1	Завершить интервью	2025-08-31 02:48:25.747565+00	2025-08-31 02:48:25.747565+00
\.


--
-- Data for Name: session_context; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.session_context (id, session_id, skill_assessments, negative_responses, current_path, context_data, current_node_id, scenario_id, created_at, updated_at, contextual_questions) FROM stdin;
ctx_14a933ae-4de6-4a7b-a832-06c0ad271b14	14a933ae-4de6-4a7b-a832-06c0ad271b14	{}	{}	[]	{}	question_1	SCENARIO_844827A6	2025-08-31 18:22:50.507264+00	2025-08-31 18:22:50.529066+00	\N
ctx_test	1618ced8-05b7-49b3-904d-c3ce08b58533	{}	{}	[]	{}	SCENARIO_917B6C27_node_1	SCENARIO_A9DB7161	2025-08-31 18:25:52.438421+00	2025-08-31 18:26:01.555144+00	{"SCENARIO_917B6C27_node_1": {"asked_questions": [], "generated_questions": ["Какие ключевые элементы вы включаете в техническую документацию при разработке бизнес-требований? Можете ли привести пример сложного требования и описать, как вы его структурировали в документации?"], "remaining_questions": ["Какие ключевые элементы вы включаете в техническую документацию при разработке бизнес-требований? Можете ли привести пример сложного требования и описать, как вы его структурировали в документации?"]}}
ctx_ba_test	bf89bae1-9ff1-47d7-bf85-ccca6b0beb3e	{}	{}	[]	{}	SCENARIO_917B6C27_node_1	SCENARIO_A9DB7161	2025-08-31 18:37:15.020796+00	2025-08-31 18:37:26.19625+00	{"SCENARIO_917B6C27_node_1": {"asked_questions": [], "generated_questions": ["Какие ключевые аспекты вы учитываете при подготовке бизнес-требований для оптимизации мониторинга мошеннических операций? Приведите пример из вашего опыта."], "remaining_questions": ["Какие ключевые аспекты вы учитываете при подготовке бизнес-требований для оптимизации мониторинга мошеннических операций? Приведите пример из вашего опыта."]}}
ctx_it_test	bc2af68a-a3fb-421f-a5c1-54cf103a5c5e	{}	{}	[]	{}	SCENARIO_85FE7B54_node_1	SCENARIO_A0EE5ADE	2025-08-31 18:38:07.16083+00	2025-08-31 18:38:33.044109+00	{"SCENARIO_85FE7B54_node_1": {"asked_questions": [], "generated_questions": [], "remaining_questions": []}}
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.sessions (id, candidate_id, vacancy_id, status, started_at, finished_at, total_score, current_step, created_at, updated_at, phone, email, total_steps, pass_rate, vacancy_code) FROM stdin;
SESS_001	1	SWE_BACK_001	completed	2025-01-15 10:00:00+00	2025-01-15 10:25:00+00	0.82	8	2025-08-27 16:41:06.414942+00	2025-08-30 14:58:16.375689+00	\N	\N	0	\N	SWE-BACK-2025-001
c55aab56-a42f-45a7-afd8-59f4b81383b7	\N	SWE_BACK_001	completed	\N	2025-08-30 16:55:32.179+00	\N	0	2025-08-30 16:54:24.796381+00	2025-08-30 16:55:32.193601+00	+7-999-999-99-99	candidate@example.com	8	\N	SWE-BACK-2025-001
153c687f-a592-47dc-a577-3dc60170d9ff	\N	SWE_BACK_001	created	\N	\N	\N	0	2025-08-30 17:52:29.653524+00	2025-08-30 17:52:29.653524+00	+7-999-999-99-99	candidate@example.com	8	\N	SWE-BACK-2025-001
fe47e667-ea4f-4d83-abc9-58a81295a685	\N	SWE_BACK_001	created	\N	\N	\N	0	2025-08-30 21:21:40.629811+00	2025-08-30 21:21:40.629811+00	+7-999-999-99-99	candidate@example.com	8	\N	SWE-BACK-2025-001
dd299d81-63b2-42f5-a10f-8af6bb8176d7	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 00:27:32.123134+00	2025-09-01 00:27:32.123134+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
ad597e46-2ba9-4482-bda9-b2253d60ecab	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	completed	\N	2025-08-31 00:09:24.789+00	\N	0	2025-08-31 00:07:12.343572+00	2025-08-31 00:09:24.797666+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
14a933ae-4de6-4a7b-a832-06c0ad271b14	\N	SWE_BACK_001	created	\N	\N	\N	0	2025-08-31 18:21:08.801935+00	2025-08-31 18:21:08.801935+00	+7-999-123-45-67	test@example.com	8	\N	SWE-BACK-2025-001
1618ced8-05b7-49b3-904d-c3ce08b58533	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-08-31 18:23:57.496978+00	2025-08-31 18:23:57.496978+00	+7-999-123-45-68	test2@example.com	8	\N	BA-2025-001
bf89bae1-9ff1-47d7-bf85-ccca6b0beb3e	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-08-31 18:37:08.471068+00	2025-08-31 18:37:08.471068+00	+7-999-111-11-11	ba_test@example.com	8	\N	BA-2025-001
bc2af68a-a3fb-421f-a5c1-54cf103a5c5e	\N	SWE_BACK_001	created	\N	\N	\N	0	2025-08-31 18:38:00.515859+00	2025-08-31 18:38:00.515859+00	+7-999-222-22-22	it_test@example.com	8	\N	SWE-BACK-2025-001
f26a8d59-b340-4a31-b07f-650f89818097	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 00:19:22.104352+00	2025-09-01 00:19:22.104352+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
87240571-1983-4a50-83a9-f7859a04ab30	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 00:31:16.21813+00	2025-09-01 00:31:16.21813+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
85b86496-6fcd-4bbc-98d0-2f4c5dfb6504	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 00:34:20.898515+00	2025-09-01 00:34:20.898515+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
2905ca67-8f89-4563-94d4-7f6d69efc095	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 00:49:01.219032+00	2025-09-01 00:49:01.219032+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
b7a7ee54-5ae5-45fc-8ad5-9f51ff109815	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:07:51.855126+00	2025-09-01 01:07:51.855126+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
c5f1edfb-4f41-4be9-b3b9-25f3f96c2181	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:18:11.239284+00	2025-09-01 01:18:11.239284+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
f6265ee7-76f4-41f3-bec3-228982c39989	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:29:38.356605+00	2025-09-01 01:29:38.356605+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
09a2d860-1f50-4ef2-b672-758e4e5f2251	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:39:28.481063+00	2025-09-01 01:39:28.481063+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
f5cd87a5-0f3e-406e-a8d7-c396361d0d4e	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:46:44.433437+00	2025-09-01 01:46:44.433437+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
f14d28f8-66f1-4561-868f-33562e86667b	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:55:46.277204+00	2025-09-01 01:55:46.277204+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
deefc08e-a5bd-46ff-9867-55ad65b926bd	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 01:59:05.734062+00	2025-09-01 01:59:05.734062+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
4405afed-77ba-4097-b747-a6a943bffdb5	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 02:13:27.879881+00	2025-09-01 02:13:27.879881+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
7512198e-12c1-40b7-a1dd-f43304763bd2	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 02:19:28.445932+00	2025-09-01 02:19:28.445932+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
8e1870ea-ef13-4dcf-b5d3-a6c713c9ba87	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-01 02:28:23.118411+00	2025-09-01 02:28:23.118411+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
6c7f12f9-900e-4923-a77f-2343fde92706	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 22:20:02.121917+00	2025-09-02 22:20:02.121917+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
d8d73a6b-9a61-41ed-86f8-b31a3cf2fcf3	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 22:33:44.902684+00	2025-09-02 22:33:44.902684+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
988d6943-2d17-48f7-812a-830a6ea12fb4	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 22:44:24.523296+00	2025-09-02 22:44:24.523296+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
8a3d7e46-2986-4002-9211-891c507f1329	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 22:53:50.962636+00	2025-09-02 22:53:50.962636+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
afcc1a86-e4bd-4aef-bb2d-8fddfe42a9db	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 23:15:54.744142+00	2025-09-02 23:15:54.744142+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
3538c3c2-5583-4034-a755-bbcdc555534f	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 23:29:37.273453+00	2025-09-02 23:29:37.273453+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
688a2ae9-c388-4068-b370-305442187aa5	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-02 23:53:08.233334+00	2025-09-02 23:53:08.233334+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
f336f13d-065b-4465-a06d-73bde6cef558	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-03 00:02:10.97901+00	2025-09-03 00:02:10.97901+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
8ea0a596-7bea-4690-8a55-545ae125cb79	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-03 00:18:08.077277+00	2025-09-03 00:18:08.077277+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
7a80becf-5f55-4231-b65f-0272ecb5e8c1	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-03 00:22:28.796203+00	2025-09-03 00:22:28.796203+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
dae0342d-3e1a-4094-9fbb-42f68b9257e6	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-03 00:41:21.090208+00	2025-09-03 00:41:21.090208+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
eb4d49d9-a3f5-4357-8229-b2aaf89a5f10	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-03 10:52:05.884278+00	2025-09-03 10:52:05.884278+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
4fc694e8-bcc9-4b4e-a074-4266ece4873f	\N	SWE_BACK_001	created	\N	\N	\N	0	2025-09-03 18:51:42.142677+00	2025-09-03 18:51:42.142677+00	+7-999-999-99-99	candidate@example.com	8	\N	SWE-BACK-2025-001
d9d06d6a-9d2a-42df-8fac-cc572c69a580	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-03 18:53:55.257072+00	2025-09-03 18:53:55.257072+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
c6942653-d339-40c1-9594-9084dd46b10f	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-07 19:40:00.587934+00	2025-09-07 19:40:00.587934+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
aba2d9c0-8e50-4212-bd36-46843f1e2113	\N	af625a8d-1f69-4aea-9d2f-2d5b504ef215	created	\N	\N	\N	0	2025-09-07 22:33:54.57962+00	2025-09-07 22:33:54.57962+00	+7-999-999-99-99	candidate@example.com	8	\N	BA-2025-001
6912a995-49ad-40e4-96e2-48e1a4f113c0	\N	SWE_BACK_001	created	\N	\N	\N	0	2025-09-08 16:04:47.982943+00	2025-09-08 16:04:47.982943+00	+7-999-999-99-99	candidate@example.com	8	\N	SWE-BACK-2025-001
\.


--
-- Data for Name: vacancies; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.vacancies (id, title, description, created_at, updated_at, vacancy_code, status, region, city, address, employment_type, contract_type, work_schedule, business_trips, salary_min, salary_max, total_income, annual_bonus_percent, bonus_description, responsibilities, requirements, education_level, experience_required, special_programs, computer_skills, foreign_languages, language_level, additional_info) FROM stdin;
SWE_BACK_001	IT-специалист	нет	2025-08-27 16:41:06.405605+00	2025-08-30 23:24:22.982917+00	SWE-BACK-2025-001	active	Санкт-Петербург	Санкт-Петербург	Маршала Говорова,52,А	full	employment	Комбинированный (гибридный) формат работы	t	150000.00	25000.00	180000.00	25.00	Годовое	Монтаж / демонтаж серверного и сетевого оборудования в ЦОД Подключение серверного и сетевого оборудования к сетям передачи данных (LAN и SAN) Первичная настройка серверного оборудования (BIOS, BMC, RAID и т.п.) Решение инцидентов/аварий в оборудовании х86 Поддержание порядка в серверных помещениях Внесение данных о проделанной работе в системы учёта (CMDB, DCIM и т.п) Сопровождение работ подрядчиков в ЦОД \n	Базовые знания об устройстве и принципах работы: - серверного оборудования х86, - структурированных кабельных систем (медных и оптических) - сетях передачи и хранения данных (LAN и SAN) - центров обработки данных Навык первичной диагностики серверного оборудования х86 Уверенные навыки работы с Excel, Word, Visio Грамотная устная и письменная речь Ответственность, аккуратность в работе, исполнительность, инициативность \n	vocational	1_year	нет	нет	Русский	fluent	\N
af625a8d-1f69-4aea-9d2f-2d5b504ef215	Business Analyst	нет	2025-08-30 14:00:12.571874+00	2025-08-30 21:45:31.256748+00	BA-2025-001	active	Москва	Москва	Пресненская,10	full	employment	5/2 в офисе	f	100000.00	150000.00	\N	10.00	премирование по KPI	- управление комплексом Системы противодействия мошенничеству и вспомогательными инструментами по управлению рисками по каналам: платежные карты/ДБО ЮЛ; - формирование предложений по оптимизации, улучшению правил антифрод-мониторинга; - участие в проектах по развитию комплекса банковских систем по противодействию мошенничеству; - анализ и формирование функциональных и бизнес-требований, постановка задач разработчику; - участие в разработке тест-кейсов и функциональных тестированиях; 	- Высшее техническое или экономическое образование; - Уверенное владение Microsoft Word, Microsoft Excel, Microsoft PowerPoint; - Навыки подготовки бизнес-требований к развитию систем; Будет преимуществом: •\\tОпыт работы с программным обеспечением в области антифрод, ПОД/ФТ-систем; •\\tОпыт работы с операциями по корпоративным картам; •\\tЗнание плана счетов клиентов ЮЛ; •\\tПредставление о клиентском пути клиента ЮЛ в банке; •\\tОпыт работы с фронтальными системами ДБО клиентов; •\\tПонимание сценариев проведения мошеннических операций и методов противодействия; •\\tНавыки разработки технической документации (ФТ, ТЗ, руководства, методики и пр.); •\\tПонимание принципов работы с СУБД •\\tЗнание основных технологий и протоколов, применяемых при разработке ПО •\\tЗнание правил платёжных систем, логики проведения транзакций по картам, в ДБО. \n	higher	3_years	нет требований	нет требований	русский	fluent	нет
\.


--
-- Data for Name: vacancy_questions; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.vacancy_questions (vacancy_id, question_id, step_no, question_weight, must_have, created_at) FROM stdin;
SWE_BACK_001	Q_FASTAPI_01	1	1.00	t	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_ASYNCIO_01	2	0.80	f	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_DATABASE_01	3	0.90	f	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_TESTING_01	4	0.70	f	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_MICROSERVICES_01	5	0.80	f	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_DEPLOYMENT_01	6	0.60	f	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_PROBLEM_SOLVING_01	7	0.90	f	2025-08-27 16:41:06.408828+00
SWE_BACK_001	Q_TEAMWORK_01	8	0.70	f	2025-08-27 16:41:06.408828+00
\.


--
-- Data for Name: vacancy_section_keywords; Type: TABLE DATA; Schema: public; Owner: interview_user
--

COPY public.vacancy_section_keywords (id, vacancy_id, section_type, keywords, confidence_score, extraction_date, created_at, updated_at) FROM stdin;
KEYWORDS_45FB0E96	SWE_BACK_001	REQUIREMENTS	["\\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0435 \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u044586", "\\u0441\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0435 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b", "\\u043c\\u0435\\u0434\\u043d\\u044b\\u0435 \\u043a\\u0430\\u0431\\u0435\\u043b\\u0438", "\\u043e\\u043f\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0435 \\u043a\\u0430\\u0431\\u0435\\u043b\\u0438", "LAN", "SAN", "\\u0446\\u0435\\u043d\\u0442\\u0440\\u044b \\u043e\\u0431\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "\\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f", "Excel", "Word", "Visio", "\\u0433\\u0440\\u0430\\u043c\\u043e\\u0442\\u043d\\u0430\\u044f \\u0443\\u0441\\u0442\\u043d\\u0430\\u044f \\u0440\\u0435\\u0447\\u044c", "\\u0433\\u0440\\u0430\\u043c\\u043e\\u0442\\u043d\\u0430\\u044f \\u043f\\u0438\\u0441\\u044c\\u043c\\u0435\\u043d\\u043d\\u0430\\u044f \\u0440\\u0435\\u0447\\u044c", "\\u043e\\u0442\\u0432\\u0435\\u0442\\u0441\\u0442\\u0432\\u0435\\u043d\\u043d\\u043e\\u0441\\u0442\\u044c", "\\u0430\\u043a\\u043a\\u0443\\u0440\\u0430\\u0442\\u043d\\u043e\\u0441\\u0442\\u044c", "\\u0438\\u043d\\u0438\\u0446\\u0438\\u0430\\u0442\\u0438\\u0432\\u043d\\u043e\\u0441\\u0442\\u044c"]	0.85	2025-08-30 22:40:15.244299+00	2025-08-30 22:40:12.569314+00	2025-08-30 22:40:12.569314+00
KEYWORDS_C30DAEA5	af625a8d-1f69-4aea-9d2f-2d5b504ef215	RESPONSIBILITIES	["\\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u0435", "\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430 \\u043f\\u0440\\u043e\\u0442\\u0438\\u0432\\u043e\\u0434\\u0435\\u0439\\u0441\\u0442\\u0432\\u0438\\u044f \\u043c\\u043e\\u0448\\u0435\\u043d\\u043d\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u0443", "\\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0440\\u0438\\u0441\\u043a\\u0430\\u043c\\u0438", "\\u043e\\u043f\\u0442\\u0438\\u043c\\u0438\\u0437\\u0430\\u0446\\u0438\\u044f", "\\u0430\\u043d\\u0442\\u0438\\u0444\\u0440\\u043e\\u0434-\\u043c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433", "\\u0443\\u0447\\u0430\\u0441\\u0442\\u0438\\u0435 \\u0432 \\u043f\\u0440\\u043e\\u0435\\u043a\\u0442\\u0430\\u0445", "\\u0430\\u043d\\u0430\\u043b\\u0438\\u0437 \\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439", "\\u0444\\u043e\\u0440\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439", "\\u043f\\u043e\\u0441\\u0442\\u0430\\u043d\\u043e\\u0432\\u043a\\u0430 \\u0437\\u0430\\u0434\\u0430\\u0447", "\\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0430 \\u0442\\u0435\\u0441\\u0442-\\u043a\\u0435\\u0439\\u0441\\u043e\\u0432", "\\u0444\\u0443\\u043d\\u043a\\u0446\\u0438\\u043e\\u043d\\u0430\\u043b\\u044c\\u043d\\u043e\\u0435 \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435"]	0.9	2025-08-30 21:18:03.604317+00	2025-08-30 21:11:03.485126+00	2025-08-30 21:18:03.604328+00
KEYWORDS_3D39911C	af625a8d-1f69-4aea-9d2f-2d5b504ef215	REQUIREMENTS	["\\u0432\\u044b\\u0441\\u0448\\u0435\\u0435 \\u0442\\u0435\\u0445\\u043d\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0435 \\u043e\\u0431\\u0440\\u0430\\u0437\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435", "\\u0432\\u044b\\u0441\\u0448\\u0435\\u0435 \\u044d\\u043a\\u043e\\u043d\\u043e\\u043c\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0435 \\u043e\\u0431\\u0440\\u0430\\u0437\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435", "Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint", "\\u043f\\u043e\\u0434\\u0433\\u043e\\u0442\\u043e\\u0432\\u043a\\u0430 \\u0431\\u0438\\u0437\\u043d\\u0435\\u0441-\\u0442\\u0440\\u0435\\u0431\\u043e\\u0432\\u0430\\u043d\\u0438\\u0439", "\\u0430\\u043d\\u0442\\u0438\\u0444\\u0440\\u043e\\u0434 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b", "\\u041f\\u041e\\u0414/\\u0424\\u0422-\\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b", "\\u043e\\u043f\\u0435\\u0440\\u0430\\u0446\\u0438\\u0438 \\u043f\\u043e \\u043a\\u043e\\u0440\\u043f\\u043e\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u044b\\u043c \\u043a\\u0430\\u0440\\u0442\\u0430\\u043c", "\\u043f\\u043b\\u0430\\u043d \\u0441\\u0447\\u0435\\u0442\\u043e\\u0432 \\u043a\\u043b\\u0438\\u0435\\u043d\\u0442\\u043e\\u0432 \\u042e\\u041b", "\\u043a\\u043b\\u0438\\u0435\\u043d\\u0442\\u0441\\u043a\\u0438\\u0439 \\u043f\\u0443\\u0442\\u044c \\u043a\\u043b\\u0438\\u0435\\u043d\\u0442\\u0430 \\u042e\\u041b", "\\u0444\\u0440\\u043e\\u043d\\u0442\\u0430\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b \\u0414\\u0411\\u041e", "\\u043c\\u043e\\u0448\\u0435\\u043d\\u043d\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0435 \\u043e\\u043f\\u0435\\u0440\\u0430\\u0446\\u0438\\u0438", "\\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0430 \\u0442\\u0435\\u0445\\u043d\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0439 \\u0434\\u043e\\u043a\\u0443\\u043c\\u0435\\u043d\\u0442\\u0430\\u0446\\u0438\\u0438", "\\u0421\\u0423\\u0411\\u0414"]	0.85	2025-08-30 21:18:32.018359+00	2025-08-30 21:15:20.556291+00	2025-08-30 21:18:32.018365+00
KEYWORDS_172C693D	SWE_BACK_001	RESPONSIBILITIES	["\\u043c\\u043e\\u043d\\u0442\\u0430\\u0436", "\\u0434\\u0435\\u043c\\u043e\\u043d\\u0442\\u0430\\u0436", "\\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u043e\\u0435 \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435", "\\u0441\\u0435\\u0442\\u0435\\u0432\\u043e\\u0435 \\u043e\\u0431\\u043e\\u0440\\u0443\\u0434\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435", "\\u043f\\u043e\\u0434\\u043a\\u043b\\u044e\\u0447\\u0435\\u043d\\u0438\\u0435", "\\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0430", "BIOS", "BMC", "RAID", "\\u0440\\u0435\\u0448\\u0435\\u043d\\u0438\\u0435 \\u0438\\u043d\\u0446\\u0438\\u0434\\u0435\\u043d\\u0442\\u043e\\u0432", "\\u0430\\u0432\\u0430\\u0440\\u0438\\u0438", "\\u043f\\u043e\\u0440\\u044f\\u0434\\u043e\\u043a", "\\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043d\\u044b\\u0435 \\u043f\\u043e\\u043c\\u0435\\u0449\\u0435\\u043d\\u0438\\u044f", "\\u0443\\u0447\\u0451\\u0442 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "CMDB", "DCIM", "\\u0441\\u043e\\u043f\\u0440\\u043e\\u0432\\u043e\\u0436\\u0434\\u0435\\u043d\\u0438\\u0435 \\u043f\\u043e\\u0434\\u0440\\u044f\\u0434\\u0447\\u0438\\u043a\\u043e\\u0432"]	0.9	2025-08-30 22:40:08.613599+00	2025-08-30 22:40:06.19512+00	2025-08-30 22:40:06.19512+00
\.


--
-- Name: candidates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: interview_user
--

SELECT pg_catalog.setval('public.candidates_id_seq', 6, true);


--
-- Name: media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: interview_user
--

SELECT pg_catalog.setval('public.media_id_seq', 1, false);


--
-- Name: qa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: interview_user
--

SELECT pg_catalog.setval('public.qa_id_seq', 57, true);


--
-- Name: qa_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: interview_user
--

SELECT pg_catalog.setval('public.qa_scores_id_seq', 22, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: candidates candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_pkey PRIMARY KEY (id);


--
-- Name: contextual_questions contextual_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.contextual_questions
    ADD CONSTRAINT contextual_questions_pkey PRIMARY KEY (id);


--
-- Name: criteria criteria_code_key; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.criteria
    ADD CONSTRAINT criteria_code_key UNIQUE (code);


--
-- Name: criteria criteria_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.criteria
    ADD CONSTRAINT criteria_pkey PRIMARY KEY (id);


--
-- Name: dynamic_criteria dynamic_criteria_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.dynamic_criteria
    ADD CONSTRAINT dynamic_criteria_pkey PRIMARY KEY (id);


--
-- Name: interview_codes interview_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.interview_codes
    ADD CONSTRAINT interview_codes_code_key UNIQUE (code);


--
-- Name: interview_codes interview_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.interview_codes
    ADD CONSTRAINT interview_codes_pkey PRIMARY KEY (id);


--
-- Name: interview_scenarios interview_scenarios_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.interview_scenarios
    ADD CONSTRAINT interview_scenarios_pkey PRIMARY KEY (id);


--
-- Name: media media_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: qa qa_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa
    ADD CONSTRAINT qa_pkey PRIMARY KEY (id);


--
-- Name: qa_scores qa_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa_scores
    ADD CONSTRAINT qa_scores_pkey PRIMARY KEY (id);


--
-- Name: question_criteria question_criteria_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.question_criteria
    ADD CONSTRAINT question_criteria_pkey PRIMARY KEY (question_id, criterion_id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: resume_blocks resume_blocks_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.resume_blocks
    ADD CONSTRAINT resume_blocks_pkey PRIMARY KEY (id);


--
-- Name: resume_skills resume_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.resume_skills
    ADD CONSTRAINT resume_skills_pkey PRIMARY KEY (id);


--
-- Name: resumes resumes_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.resumes
    ADD CONSTRAINT resumes_pkey PRIMARY KEY (id);


--
-- Name: scenario_criteria_mappings scenario_criteria_mappings_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_criteria_mappings
    ADD CONSTRAINT scenario_criteria_mappings_pkey PRIMARY KEY (id);


--
-- Name: scenario_nodes scenario_nodes_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_nodes
    ADD CONSTRAINT scenario_nodes_pkey PRIMARY KEY (id);


--
-- Name: scenario_transitions scenario_transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_transitions
    ADD CONSTRAINT scenario_transitions_pkey PRIMARY KEY (id);


--
-- Name: session_context session_context_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.session_context
    ADD CONSTRAINT session_context_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: vacancies vacancies_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.vacancies
    ADD CONSTRAINT vacancies_pkey PRIMARY KEY (id);


--
-- Name: vacancy_questions vacancy_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.vacancy_questions
    ADD CONSTRAINT vacancy_questions_pkey PRIMARY KEY (vacancy_id, question_id);


--
-- Name: vacancy_section_keywords vacancy_section_keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.vacancy_section_keywords
    ADD CONSTRAINT vacancy_section_keywords_pkey PRIMARY KEY (id);


--
-- Name: idx_interview_codes_code; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX idx_interview_codes_code ON public.interview_codes USING btree (code);


--
-- Name: ix_candidates_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_candidates_id ON public.candidates USING btree (id);


--
-- Name: ix_contextual_questions_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_contextual_questions_id ON public.contextual_questions USING btree (id);


--
-- Name: ix_criteria_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_criteria_id ON public.criteria USING btree (id);


--
-- Name: ix_interview_scenarios_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_interview_scenarios_id ON public.interview_scenarios USING btree (id);


--
-- Name: ix_media_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_media_id ON public.media USING btree (id);


--
-- Name: ix_messages_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_messages_id ON public.messages USING btree (id);


--
-- Name: ix_qa_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_qa_id ON public.qa USING btree (id);


--
-- Name: ix_qa_scores_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_qa_scores_id ON public.qa_scores USING btree (id);


--
-- Name: ix_questions_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_questions_id ON public.questions USING btree (id);


--
-- Name: ix_resume_blocks_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_resume_blocks_id ON public.resume_blocks USING btree (id);


--
-- Name: ix_resume_skills_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_resume_skills_id ON public.resume_skills USING btree (id);


--
-- Name: ix_resumes_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_resumes_id ON public.resumes USING btree (id);


--
-- Name: ix_scenario_nodes_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_scenario_nodes_id ON public.scenario_nodes USING btree (id);


--
-- Name: ix_scenario_transitions_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_scenario_transitions_id ON public.scenario_transitions USING btree (id);


--
-- Name: ix_session_context_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_session_context_id ON public.session_context USING btree (id);


--
-- Name: ix_sessions_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_sessions_id ON public.sessions USING btree (id);


--
-- Name: ix_sessions_vacancy_code; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_sessions_vacancy_code ON public.sessions USING btree (vacancy_code);


--
-- Name: ix_vacancies_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_vacancies_id ON public.vacancies USING btree (id);


--
-- Name: ix_vacancies_vacancy_code; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE UNIQUE INDEX ix_vacancies_vacancy_code ON public.vacancies USING btree (vacancy_code);


--
-- Name: ix_vacancy_section_keywords_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_vacancy_section_keywords_id ON public.vacancy_section_keywords USING btree (id);


--
-- Name: ix_vacancy_section_keywords_section_type; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_vacancy_section_keywords_section_type ON public.vacancy_section_keywords USING btree (section_type);


--
-- Name: ix_vacancy_section_keywords_vacancy_id; Type: INDEX; Schema: public; Owner: interview_user
--

CREATE INDEX ix_vacancy_section_keywords_vacancy_id ON public.vacancy_section_keywords USING btree (vacancy_id);


--
-- Name: candidates update_candidates_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON public.candidates FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: criteria update_criteria_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_criteria_updated_at BEFORE UPDATE ON public.criteria FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: qa_scores update_qa_scores_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_qa_scores_updated_at BEFORE UPDATE ON public.qa_scores FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: qa update_qa_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_qa_updated_at BEFORE UPDATE ON public.qa FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: questions update_questions_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON public.questions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: sessions update_sessions_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON public.sessions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: vacancies update_vacancies_updated_at; Type: TRIGGER; Schema: public; Owner: interview_user
--

CREATE TRIGGER update_vacancies_updated_at BEFORE UPDATE ON public.vacancies FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: contextual_questions contextual_questions_scenario_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.contextual_questions
    ADD CONSTRAINT contextual_questions_scenario_node_id_fkey FOREIGN KEY (scenario_node_id) REFERENCES public.scenario_nodes(id);


--
-- Name: contextual_questions contextual_questions_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.contextual_questions
    ADD CONSTRAINT contextual_questions_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: dynamic_criteria dynamic_criteria_vacancy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.dynamic_criteria
    ADD CONSTRAINT dynamic_criteria_vacancy_id_fkey FOREIGN KEY (vacancy_id) REFERENCES public.vacancies(id);


--
-- Name: interview_codes interview_codes_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.interview_codes
    ADD CONSTRAINT interview_codes_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.resumes(id);


--
-- Name: interview_scenarios interview_scenarios_vacancy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.interview_scenarios
    ADD CONSTRAINT interview_scenarios_vacancy_id_fkey FOREIGN KEY (vacancy_id) REFERENCES public.vacancies(id);


--
-- Name: media media_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: messages messages_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: qa qa_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa
    ADD CONSTRAINT qa_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: qa_scores qa_scores_criterion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa_scores
    ADD CONSTRAINT qa_scores_criterion_id_fkey FOREIGN KEY (criterion_id) REFERENCES public.criteria(id);


--
-- Name: qa_scores qa_scores_qa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa_scores
    ADD CONSTRAINT qa_scores_qa_id_fkey FOREIGN KEY (qa_id) REFERENCES public.qa(id);


--
-- Name: qa qa_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.qa
    ADD CONSTRAINT qa_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: question_criteria question_criteria_criterion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.question_criteria
    ADD CONSTRAINT question_criteria_criterion_id_fkey FOREIGN KEY (criterion_id) REFERENCES public.criteria(id);


--
-- Name: question_criteria question_criteria_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.question_criteria
    ADD CONSTRAINT question_criteria_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: resume_blocks resume_blocks_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.resume_blocks
    ADD CONSTRAINT resume_blocks_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.resumes(id);


--
-- Name: resume_skills resume_skills_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.resume_skills
    ADD CONSTRAINT resume_skills_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.resumes(id);


--
-- Name: resumes resumes_vacancy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.resumes
    ADD CONSTRAINT resumes_vacancy_id_fkey FOREIGN KEY (vacancy_id) REFERENCES public.vacancies(id);


--
-- Name: scenario_criteria_mappings scenario_criteria_mappings_criterion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_criteria_mappings
    ADD CONSTRAINT scenario_criteria_mappings_criterion_id_fkey FOREIGN KEY (criterion_id) REFERENCES public.dynamic_criteria(id);


--
-- Name: scenario_criteria_mappings scenario_criteria_mappings_scenario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_criteria_mappings
    ADD CONSTRAINT scenario_criteria_mappings_scenario_id_fkey FOREIGN KEY (scenario_id) REFERENCES public.interview_scenarios(id);


--
-- Name: scenario_nodes scenario_nodes_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_nodes
    ADD CONSTRAINT scenario_nodes_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: scenario_nodes scenario_nodes_scenario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_nodes
    ADD CONSTRAINT scenario_nodes_scenario_id_fkey FOREIGN KEY (scenario_id) REFERENCES public.interview_scenarios(id);


--
-- Name: scenario_transitions scenario_transitions_from_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_transitions
    ADD CONSTRAINT scenario_transitions_from_node_id_fkey FOREIGN KEY (from_node_id) REFERENCES public.scenario_nodes(id);


--
-- Name: scenario_transitions scenario_transitions_scenario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_transitions
    ADD CONSTRAINT scenario_transitions_scenario_id_fkey FOREIGN KEY (scenario_id) REFERENCES public.interview_scenarios(id);


--
-- Name: scenario_transitions scenario_transitions_to_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.scenario_transitions
    ADD CONSTRAINT scenario_transitions_to_node_id_fkey FOREIGN KEY (to_node_id) REFERENCES public.scenario_nodes(id);


--
-- Name: session_context session_context_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.session_context
    ADD CONSTRAINT session_context_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: sessions sessions_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: sessions sessions_vacancy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_vacancy_id_fkey FOREIGN KEY (vacancy_id) REFERENCES public.vacancies(id);


--
-- Name: vacancy_questions vacancy_questions_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.vacancy_questions
    ADD CONSTRAINT vacancy_questions_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: vacancy_questions vacancy_questions_vacancy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.vacancy_questions
    ADD CONSTRAINT vacancy_questions_vacancy_id_fkey FOREIGN KEY (vacancy_id) REFERENCES public.vacancies(id);


--
-- Name: vacancy_section_keywords vacancy_section_keywords_vacancy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: interview_user
--

ALTER TABLE ONLY public.vacancy_section_keywords
    ADD CONSTRAINT vacancy_section_keywords_vacancy_id_fkey FOREIGN KEY (vacancy_id) REFERENCES public.vacancies(id);


--
-- PostgreSQL database dump complete
--

\unrestrict EB9Hk4vyQk3x3BKW8ZbeFLT5BUXDzUnVhXXJafafngrmu2Meo5xCahlet9rKqHM

