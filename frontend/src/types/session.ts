// Interview session types
export type SessionStatus = 'created' | 'in_progress' | 'completed' | 'failed' | 'cancelled'

export interface InterviewSession {
  id: string
  vacancyId: string
  candidateInfo: CandidateInfo
  status: SessionStatus
  currentStep: number
  totalSteps: number
  responses: InterviewResponse[]
  scores: SessionScores
  metadata: SessionMetadata
  createdAt: Date
  updatedAt: Date
  total_score?: number
}

export interface CandidateInfo {
  phone: string
  email?: string
  name?: string
  resumeId?: string
}

export interface InterviewResponse {
  id: string
  questionId: string
  question: string
  answer: string
  audioUrl?: string
  score?: number
  feedback?: string
  timestamp: Date
  duration?: number
}

export interface SessionScores {
  overall: number
  technical: number
  communication: number
  experience: number
  cultural: number
  breakdown: ScoreBreakdown[]
}

export interface ScoreBreakdown {
  category: string
  score: number
  maxScore: number
  weight: number
  feedback?: string
}

export interface SessionMetadata {
  userAgent?: string
  ipAddress?: string
  deviceType?: 'desktop' | 'mobile' | 'tablet'
  browserInfo?: string
  sessionDuration?: number
  averageResponseTime?: number
}

export interface SessionProgress {
  currentStep: number
  totalSteps: number
  completedSteps: string[]
  estimatedTimeRemaining?: number
}

// Session management types
export interface SessionAction {
  id: string
  label: string
  icon?: string
  action: () => void
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
}

export interface SessionFilters {
  status?: SessionStatus[]
  vacancyId?: string
  dateRange?: {
    start: Date
    end: Date
  }
  scoreRange?: {
    min: number
    max: number
  }
}

export interface SessionExportOptions {
  format: 'json' | 'csv' | 'pdf'
  includeResponses: boolean
  includeScores: boolean
  includeMetadata: boolean
}