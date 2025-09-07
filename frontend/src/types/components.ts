// Enhanced Component Types for Design System

// Base component props with design system integration
export type ComponentSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type ComponentVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success' | 'warning' | 'info';
export type ComponentColor = 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info' | 'neutral';

// Icon types
export interface IconProps {
  name: string;
  size?: ComponentSize | number;
  color?: ComponentColor | string;
  spin?: boolean;
}

// Enhanced Button Component
export interface EnhancedButtonProps {
  variant?: ComponentVariant;
  size?: ComponentSize;
  color?: ComponentColor;
  loading?: boolean;
  disabled?: boolean;
  block?: boolean;
  rounded?: boolean | 'sm' | 'md' | 'lg' | 'full';
  elevation?: 0 | 1 | 2 | 3 | 4 | 5;
  
  // Icon props
  icon?: string;
  iconPosition?: 'left' | 'right';
  iconOnly?: boolean;
  
  // Link props
  to?: string | object;
  href?: string;
  target?: '_blank' | '_self' | '_parent' | '_top';
  
  // HTML attributes
  type?: 'button' | 'submit' | 'reset';
  form?: string;
  
  // Events
  onClick?: (event: MouseEvent) => void;
}

// Enhanced Input Components
export interface EnhancedInputProps {
  modelValue?: string | number;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'textarea';
  label?: string;
  placeholder?: string;
  hint?: string;
  error?: string | string[];
  success?: string;
  
  // Validation
  required?: boolean;
  rules?: EnhancedValidationRule[];
  
  // State
  disabled?: boolean;
  readonly?: boolean;
  loading?: boolean;
  
  // Appearance
  size?: ComponentSize;
  variant?: 'outlined' | 'filled' | 'underlined' | 'plain';
  density?: 'default' | 'comfortable' | 'compact';
  
  // Icons and actions
  prependIcon?: string;
  appendIcon?: string;
  clearable?: boolean;
  
  // Input specific
  maxlength?: number;
  minlength?: number;
  autocomplete?: string;
  
  // Events
  'onUpdate:modelValue'?: (value: string | number) => void;
  onFocus?: (event: FocusEvent) => void;
  onBlur?: (event: FocusEvent) => void;
  onChange?: (event: Event) => void;
}

export interface BaseSelectProps extends Omit<EnhancedInputProps, 'type'> {
  items: SelectItem[];
  multiple?: boolean;
  chips?: boolean;
  closableChips?: boolean;
  itemTitle?: string | ((item: any) => string);
  itemValue?: string | ((item: any) => any);
  returnObject?: boolean;
  
  // Search and filtering
  filterable?: boolean;
  noFilter?: boolean;
  customFilter?: (item: any, queryText: string, itemText: string) => boolean;
  
  // Menu props
  menuProps?: Record<string, any>;
  openOnClear?: boolean;
}

export interface SelectItem {
  title: string;
  value: any;
  props?: Record<string, any>;
  disabled?: boolean;
  divider?: boolean;
  header?: string;
}

// Enhanced Card Component
export interface EnhancedCardProps {
  title?: string;
  subtitle?: string;
  text?: string;
  
  // Appearance
  variant?: 'elevated' | 'flat' | 'tonal' | 'outlined' | 'plain';
  color?: ComponentColor;
  elevation?: 0 | 1 | 2 | 3 | 4 | 5;
  rounded?: boolean | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  
  // Layout
  width?: string | number;
  height?: string | number;
  maxWidth?: string | number;
  maxHeight?: string | number;
  
  // Interactive
  hover?: boolean;
  ripple?: boolean;
  link?: boolean;
  to?: string | object;
  href?: string;
  
  // Loading state
  loading?: boolean;
  
  // Actions
  actions?: EnhancedCardAction[];
  
  // Events
  onClick?: (event: MouseEvent) => void;
}

export interface EnhancedCardAction {
  label: string;
  icon?: string;
  variant?: ComponentVariant;
  color?: ComponentColor;
  disabled?: boolean;
  loading?: boolean;
  onClick: () => void | Promise<void>;
}

// Modal and Dialog Components
export interface EnhancedModalProps {
  modelValue: boolean;
  title?: string;
  
  // Size and positioning
  width?: string | number;
  maxWidth?: string | number;
  height?: string | number;
  maxHeight?: string | number;
  fullscreen?: boolean;
  
  // Behavior
  persistent?: boolean;
  noClickAnimation?: boolean;
  scrollable?: boolean;
  
  // Appearance
  transition?: string;
  
  // Events
  'onUpdate:modelValue'?: (value: boolean) => void;
  onAfterEnter?: () => void;
  onAfterLeave?: () => void;
}

export interface EnhancedConfirmDialogProps extends EnhancedModalProps {
  message: string;
  type?: 'info' | 'warning' | 'error' | 'success';
  confirmText?: string;
  cancelText?: string;
  confirmColor?: ComponentColor;
  onConfirm: () => void | Promise<void>;
  onCancel?: () => void;
}

// Layout Components
export interface AppLayoutProps {
  navigationDrawer?: boolean;
  navigationRail?: boolean;
  appBar?: boolean;
  footer?: boolean;
}

export interface AppBarProps {
  title?: string;
  color?: ComponentColor;
  elevation?: 0 | 1 | 2 | 3 | 4 | 5;
  flat?: boolean;
  density?: 'default' | 'comfortable' | 'compact';
  
  // Navigation
  showNavigationIcon?: boolean;
  navigationIcon?: string;
  
  // User info
  user?: EnhancedUserInfo;
  showUserMenu?: boolean;
  
  // Search
  showSearch?: boolean;
  searchPlaceholder?: string;
  
  // Breadcrumbs
  breadcrumbs?: BreadcrumbItem[];
  
  // Events
  onNavigationClick?: () => void;
  onSearch?: (query: string) => void;
}

export interface NavigationDrawerProps {
  modelValue: boolean;
  items: EnhancedNavigationItem[];
  
  // Appearance
  color?: ComponentColor;
  width?: string | number;
  rail?: boolean;
  permanent?: boolean;
  temporary?: boolean;
  
  // Behavior
  expandOnHover?: boolean;
  
  // Events
  'onUpdate:modelValue'?: (value: boolean) => void;
}

export interface EnhancedNavigationItem {
  title: string;
  value?: any;
  to?: string | object;
  href?: string;
  
  // Appearance
  prependIcon?: string;
  appendIcon?: string;
  color?: ComponentColor;
  
  // State
  active?: boolean;
  disabled?: boolean;
  
  // Hierarchy
  children?: EnhancedNavigationItem[];
  
  // Badge
  badge?: string | number;
  badgeColor?: ComponentColor;
  
  // Events
  onClick?: () => void;
}

export interface BreadcrumbItem {
  title: string;
  to?: string | object;
  href?: string;
  disabled?: boolean;
  exact?: boolean;
}

// Data Display Components
export interface DataTableProps<T = any> {
  items: T[];
  headers: DataTableHeader[];
  
  // Selection
  showSelect?: boolean;
  selectStrategy?: 'single' | 'page' | 'all';
  modelValue?: T[];
  returnObject?: boolean;
  
  // Sorting
  sortBy?: SortItem[];
  multiSort?: boolean;
  mustSort?: boolean;
  
  // Pagination
  page?: number;
  itemsPerPage?: number;
  itemsPerPageOptions?: number[];
  
  // Appearance
  density?: 'default' | 'comfortable' | 'compact';
  height?: string | number;
  fixedHeader?: boolean;
  fixedFooter?: boolean;
  
  // Loading
  loading?: boolean;
  
  // Expansion
  showExpand?: boolean;
  expandOnClick?: boolean;
  
  // Events
  'onUpdate:modelValue'?: (value: T[]) => void;
  'onUpdate:sortBy'?: (value: SortItem[]) => void;
  'onUpdate:page'?: (value: number) => void;
  'onUpdate:itemsPerPage'?: (value: number) => void;
  onItemClick?: (event: MouseEvent, item: { item: T }) => void;
}

export interface DataTableHeader {
  key: string;
  title: string;
  value?: string | ((item: any) => any);
  
  // Sorting
  sortable?: boolean;
  sort?: (a: any, b: any) => number;
  
  // Appearance
  align?: 'start' | 'center' | 'end';
  width?: string | number;
  minWidth?: string | number;
  maxWidth?: string | number;
  
  // Filtering
  filterable?: boolean;
  filter?: (value: any, query: string, item: any) => boolean;
  
  // Custom rendering
  cellProps?: Record<string, any> | ((data: { item: any; index: number }) => Record<string, any>);
  headerProps?: Record<string, any>;
}

export interface SortItem {
  key: string;
  order: 'asc' | 'desc';
}

// Form Components
export interface FormProps {
  modelValue?: Record<string, any>;
  schema?: FormSchema;
  
  // Validation
  disabled?: boolean;
  readonly?: boolean;
  validateOn?: 'blur' | 'input' | 'submit' | 'lazy';
  
  // Events
  'onUpdate:modelValue'?: (value: Record<string, any>) => void;
  onSubmit?: (values: Record<string, any>) => void | Promise<void>;
  onInvalid?: (errors: Record<string, string[]>) => void;
}

export interface FormSchema {
  fields: EnhancedFormField[];
  validation?: Record<string, EnhancedValidationRule[]>;
}

export interface EnhancedFormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'textarea' | 'select' | 'checkbox' | 'radio' | 'switch' | 'date' | 'time' | 'datetime';
  
  // Validation
  required?: boolean;
  rules?: EnhancedValidationRule[];
  
  // Appearance
  size?: ComponentSize;
  variant?: string;
  
  // Options for select/radio
  items?: SelectItem[];
  
  // Input specific
  placeholder?: string;
  hint?: string;
  
  // Layout
  cols?: number;
  sm?: number;
  md?: number;
  lg?: number;
  xl?: number;
}

export interface EnhancedValidationRule {
  message: string;
  test: (value: any) => boolean | string;
}

// Utility types
export interface EnhancedUserInfo {
  name: string;
  email?: string;
  avatar?: string;
  role?: string;
}

// Composable return types
export interface UseThemeReturn {
  theme: { value: 'light' | 'dark' };
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  isDark: { value: boolean };
}

export interface UseBreakpointsReturn {
  xs: { value: boolean };
  sm: { value: boolean };
  md: { value: boolean };
  lg: { value: boolean };
  xl: { value: boolean };
  mobile: { value: boolean };
  tablet: { value: boolean };
  desktop: { value: boolean };
  width: { value: number };
  height: { value: number };
}