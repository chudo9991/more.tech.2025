// Resume management types
export type ResumeStatus = 'uploaded' | 'processing' | 'processed' | 'failed'
export type FileFormat = 'pdf' | 'doc' | 'docx' | 'txt'

export interface Resume {
  id: string
  filename: string
  originalName: string
  fileSize: number
  format: FileFormat
  status: ResumeStatus
  candidateInfo: ResumeCandidateInfo
  extractedData?: ResumeExtractedData
  matchingScore?: number
  uploadedAt: Date
  processedAt?: Date
  downloadUrl?: string
}

export interface ResumeCandidateInfo {
  name?: string
  email?: string
  phone?: string
  location?: string
  linkedIn?: string
  github?: string
}

export interface ResumeExtractedData {
  summary?: string
  experience: WorkExperience[]
  education: Education[]
  skills: string[]
  languages: Language[]
  certifications: Certification[]
  projects: Project[]
}

export interface WorkExperience {
  company: string
  position: string
  startDate: Date
  endDate?: Date
  current: boolean
  description: string
  technologies?: string[]
  achievements?: string[]
}

export interface Education {
  institution: string
  degree: string
  field: string
  startDate: Date
  endDate?: Date
  gpa?: number
  honors?: string[]
}

export interface Language {
  name: string
  level: 'basic' | 'intermediate' | 'advanced' | 'native'
  certifications?: string[]
}

export interface Certification {
  name: string
  issuer: string
  issueDate: Date
  expiryDate?: Date
  credentialId?: string
  url?: string
}

export interface Project {
  name: string
  description: string
  technologies: string[]
  url?: string
  githubUrl?: string
  startDate?: Date
  endDate?: Date
}

// Resume matching types
export interface ResumeMatch {
  resumeId: string
  vacancyId: string
  overallScore: number
  categoryScores: CategoryScore[]
  matchedKeywords: string[]
  missingKeywords: string[]
  recommendations: string[]
  calculatedAt: Date
}

export interface CategoryScore {
  category: 'skills' | 'experience' | 'education' | 'keywords'
  score: number
  maxScore: number
  weight: number
  details: string[]
}

// Batch upload types
export interface BatchUploadResult {
  id: string
  totalFiles: number
  processedFiles: number
  successfulUploads: number
  failedUploads: number
  results: ResumeUploadResult[]
  startedAt: Date
  completedAt?: Date
}

export interface ResumeUploadResult {
  filename: string
  status: 'success' | 'failed'
  resumeId?: string
  error?: string
  fileSize: number
}