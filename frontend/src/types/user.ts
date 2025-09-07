// User management types
export type UserRole = 'admin' | 'hr' | 'interviewer' | 'candidate'

export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  avatar?: string
  preferences: UserPreferences
  createdAt: Date
  updatedAt: Date
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system'
  language: string
  notifications: NotificationSettings
  timezone?: string
}

export interface NotificationSettings {
  email: boolean
  push: boolean
  sms: boolean
  sessionUpdates: boolean
  systemAlerts: boolean
}

export interface UserInfo {
  name: string
  avatar?: string
  role: UserRole
}