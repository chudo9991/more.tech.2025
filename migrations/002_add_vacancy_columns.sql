-- Add missing columns to vacancies table

ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS vacancy_code VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active';
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS region VARCHAR(255);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS city VARCHAR(255);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS address TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS employment_type VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS contract_type VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS work_schedule VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS business_trips VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS salary_min INTEGER;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS salary_max INTEGER;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS total_income INTEGER;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS annual_bonus_percent DECIMAL(5,2);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS bonus_description TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS responsibilities TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS requirements TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS education_level VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS experience_required VARCHAR(100);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS special_programs TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS computer_skills TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS foreign_languages TEXT;
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS language_level VARCHAR(50);
ALTER TABLE vacancies ADD COLUMN IF NOT EXISTS additional_info TEXT;

-- Create index on vacancy_code if it doesn't exist
CREATE INDEX IF NOT EXISTS idx_vacancies_vacancy_code ON vacancies(vacancy_code);
CREATE INDEX IF NOT EXISTS idx_vacancies_status ON vacancies(status);