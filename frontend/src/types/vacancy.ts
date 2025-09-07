// Vacancy management types
export type EmploymentType = 'full_time' | 'part_time' | 'contract' | 'internship'
export type ExperienceLevel = 'entry' | 'junior' | 'middle' | 'senior' | 'lead'
export type VacancyStatus = 'draft' | 'active' | 'paused' | 'closed'

export interface Vacancy {
  id: string
  title: string
  description: string
  requirements: string[]
  responsibilities: string[]
  department: string
  location: string
  employmentType: EmploymentType
  experienceLevel: ExperienceLevel
  salary?: SalaryRange
  benefits?: string[]
  status: VacancyStatus
  scenarioId?: string
  createdBy: string
  createdAt: Date
  updatedAt: Date
  keywords?: VacancyKeywords
}

export interface SalaryRange {
  min: number
  max: number
  currency: string
  period: 'hour' | 'month' | 'year'
}

export interface VacancyKeywords {
  requirements: string[]
  responsibilities: string[]
  skills: string[]
  technologies: string[]
  confidenceScore?: number
  extractedAt: Date
}

export interface VacancyFormData {
  title: string
  description: string
  requirements: string[]
  responsibilities: string[]
  department: string
  location: string
  employmentType: EmploymentType
  experienceLevel: ExperienceLevel
  salary?: SalaryRange
  benefits?: string[]
}

// Scenario types
export interface Scenario {
  id: string
  vacancyId: string
  name: string
  description: string
  questions: ScenarioQuestion[]
  criteria: EvaluationCriteria[]
  estimatedDuration: number
  createdAt: Date
  updatedAt: Date
}

export interface ScenarioQuestion {
  id: string
  text: string
  type: 'technical' | 'behavioral' | 'situational'
  expectedAnswer?: string
  keywords: string[]
  weight: number
  timeLimit?: number
}

export interface EvaluationCriteria {
  id: string
  name: string
  description: string
  weight: number
  scoreRange: {
    min: number
    max: number
  }
}

// Keywords management types
export type KeywordSectionType = 'requirements' | 'responsibilities' | 'skills' | 'technologies'

export interface KeywordSection {
  sectionType: KeywordSectionType
  keywords: string[]
  confidenceScore?: number
  extractedAt: Date
}

export interface KeywordStats {
  totalKeywords: number
  sectionsExtracted: number
  averageConfidence: number
  lastUpdated: Date
}