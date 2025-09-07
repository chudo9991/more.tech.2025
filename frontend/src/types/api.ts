// API related types
export interface ApiResponse<T = any> {
  data: T
  message?: string
  status: number
  timestamp: Date
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, any>
  timestamp: Date
  context?: ErrorContext
}

export interface ErrorContext {
  component: string
  action: string
  userId?: string
  sessionId?: string
}

export type ErrorSeverity = 'low' | 'medium' | 'high' | 'critical'

// Pagination types
export interface PaginationParams {
  skip?: number
  limit?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
  hasNext: boolean
  hasPrevious: boolean
}

// Request/Response types for specific endpoints
export interface SessionsRequest extends PaginationParams {
  status?: string
  vacancy_id?: string
  date_from?: string
  date_to?: string
}

export interface VacanciesRequest extends PaginationParams {
  status?: string
  department?: string
  location?: string
}

export interface ResumesRequest extends PaginationParams {
  status?: string
  format?: string
  uploaded_from?: string
  uploaded_to?: string
}

// Statistics types
export interface HRStatistics {
  total_sessions: number
  completed_sessions: number
  in_progress_sessions: number
  avg_score: number
  sessions_change: string
  completed_change: string
  progress_change: string
  score_change: string
}

export interface SystemStatus {
  status: 'healthy' | 'degraded' | 'down'
  services: ServiceStatus[]
  lastChecked: Date
  uptime: number
}

export interface ServiceStatus {
  name: string
  status: 'up' | 'down' | 'warning'
  responseTime?: number
  lastChecked: Date
  error?: string
}

// File upload types
export interface FileUploadProgress {
  filename: string
  progress: number
  status: 'uploading' | 'processing' | 'completed' | 'failed'
  error?: string
}

export interface UploadConfig {
  maxFileSize: number
  allowedFormats: string[]
  maxFiles: number
  chunkSize?: number
}