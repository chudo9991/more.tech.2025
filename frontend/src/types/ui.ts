// UI component types
import type { UserInfo } from './user'

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
export type ButtonSize = 'sm' | 'md' | 'lg'
export type InputType = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search'
export type AlertType = 'success' | 'warning' | 'error' | 'info'

// Base component props
export interface BaseButtonProps {
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
  disabled?: boolean
  icon?: string
  iconPosition?: 'left' | 'right'
  fullWidth?: boolean
  type?: 'button' | 'submit' | 'reset'
}

export interface BaseInputProps {
  type?: InputType
  label?: string
  placeholder?: string
  error?: string
  hint?: string
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  icon?: string
  iconPosition?: 'left' | 'right'
  clearable?: boolean
}

export interface BaseCardProps {
  title?: string
  subtitle?: string
  actions?: CardAction[]
  loading?: boolean
  hoverable?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
}

export interface CardAction {
  label: string
  icon?: string
  action: () => void
  variant?: ButtonVariant
  disabled?: boolean
}

// Layout component props
export interface AppHeaderProps {
  title?: string
  showNavigation?: boolean
  user?: UserInfo
  showSearch?: boolean
  breadcrumbs?: Breadcrumb[]
}

export interface AppSidebarProps {
  collapsed?: boolean
  items: NavigationItem[]
  showToggle?: boolean
}

export interface AppFooterProps {
  showLinks?: boolean
  companyInfo?: CompanyInfo
}

// Navigation types
export interface NavigationItem {
  id: string
  label: string
  icon?: string
  route?: string
  children?: NavigationItem[]
  badge?: string | number
  disabled?: boolean
  external?: boolean
}

export interface Breadcrumb {
  label: string
  route?: string
  active?: boolean
}

export interface CompanyInfo {
  name: string
  logo?: string
  website?: string
  email?: string
  phone?: string
}

// Modal and dialog types
export interface BaseModalProps {
  visible: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  closable?: boolean
  maskClosable?: boolean
  persistent?: boolean
  loading?: boolean
}

export interface ConfirmDialogProps extends BaseModalProps {
  message: string
  confirmText?: string
  cancelText?: string
  type?: AlertType
  onConfirm: () => void
  onCancel?: () => void
}

// Form types
export interface FormField {
  name: string
  label: string
  type: InputType
  required?: boolean
  placeholder?: string
  hint?: string
  validation?: ValidationRule[]
  options?: SelectOption[]
}

export interface SelectOption {
  label: string
  value: any
  disabled?: boolean
  group?: string
}

export interface ValidationRule {
  type: 'required' | 'email' | 'min' | 'max' | 'pattern' | 'custom'
  value?: any
  message: string
  validator?: (value: any) => boolean
}

// Table types
export interface TableColumn {
  key: string
  title: string
  dataIndex?: string
  width?: number | string
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  filterable?: boolean
  render?: (value: any, record: any, index: number) => any
}

export interface TableProps {
  columns: TableColumn[]
  data: any[]
  loading?: boolean
  pagination?: PaginationConfig
  selection?: SelectionConfig
  expandable?: ExpandableConfig
}

export interface PaginationConfig {
  current: number
  pageSize: number
  total: number
  showSizeChanger?: boolean
  showQuickJumper?: boolean
  showTotal?: boolean
}

export interface SelectionConfig {
  type: 'checkbox' | 'radio'
  selectedRowKeys: string[]
  onChange: (selectedRowKeys: string[], selectedRows: any[]) => void
}

export interface ExpandableConfig {
  expandedRowKeys: string[]
  onExpand: (expanded: boolean, record: any) => void
  expandedRowRender: (record: any, index: number) => any
}

// Notification types
export interface NotificationOptions {
  type: AlertType
  title: string
  message?: string
  duration?: number
  closable?: boolean
  action?: NotificationAction
}

export interface NotificationAction {
  label: string
  action: () => void
}

// Theme types
export interface ThemeConfig {
  mode: 'light' | 'dark' | 'system'
  primaryColor: string
  borderRadius: 'none' | 'sm' | 'md' | 'lg'
  compactMode: boolean
}

// Loading states
export interface LoadingState {
  loading: boolean
  error?: string | null
  data?: any
}

// Filter and search types
export interface FilterOption {
  key: string
  label: string
  type: 'select' | 'multiselect' | 'date' | 'daterange' | 'number' | 'text'
  options?: SelectOption[]
  placeholder?: string
}

export interface SearchConfig {
  placeholder: string
  debounceMs?: number
  minLength?: number
  showSuggestions?: boolean
}

// Chart and visualization types
export interface ChartData {
  labels: string[]
  datasets: ChartDataset[]
}

export interface ChartDataset {
  label: string
  data: number[]
  backgroundColor?: string | string[]
  borderColor?: string | string[]
  borderWidth?: number
}

export interface ChartOptions {
  responsive: boolean
  maintainAspectRatio: boolean
  plugins?: any
  scales?: any
}