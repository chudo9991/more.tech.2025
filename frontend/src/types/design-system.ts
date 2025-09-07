// Design System Types
export interface ColorPalette {
  // Primary Colors
  primary: {
    50: string;
    100: string;
    200: string;
    300: string;
    400: string;
    500: string; // Main brand color
    600: string;
    700: string;
    800: string;
    900: string;
    950: string;
  };
  
  // Neutral Colors
  neutral: {
    50: string;
    100: string;
    200: string;
    300: string;
    400: string;
    500: string;
    600: string;
    700: string;
    800: string;
    900: string;
    950: string;
  };
  
  // Semantic Colors
  success: {
    50: string;
    100: string;
    500: string;
    600: string;
    700: string;
  };
  warning: {
    50: string;
    100: string;
    500: string;
    600: string;
    700: string;
  };
  error: {
    50: string;
    100: string;
    500: string;
    600: string;
    700: string;
  };
  info: {
    50: string;
    100: string;
    500: string;
    600: string;
    700: string;
  };
}

export interface TypographyScale {
  fontFamily: {
    sans: string[];
    mono: string[];
  };
  fontSize: {
    xs: string;    // 12px
    sm: string;    // 14px
    base: string;  // 16px
    lg: string;    // 18px
    xl: string;    // 20px
    '2xl': string; // 24px
    '3xl': string; // 30px
    '4xl': string; // 36px
  };
  fontWeight: {
    normal: number;
    medium: number;
    semibold: number;
    bold: number;
  };
  lineHeight: {
    tight: string;
    normal: string;
    relaxed: string;
  };
}

export interface SpacingSystem {
  spacing: {
    0: string;
    1: string;  // 4px
    2: string;  // 8px
    3: string;  // 12px
    4: string;  // 16px
    6: string;  // 24px
    8: string;  // 32px
    12: string; // 48px
    16: string; // 64px
    20: string; // 80px
  };
}

export interface BorderRadius {
  none: string;
  sm: string;
  md: string;
  lg: string;
  xl: string;
  '2xl': string;
  '3xl': string;
  full: string;
}

export interface BoxShadow {
  none: string;
  sm: string;
  md: string;
  lg: string;
  xl: string;
  soft: string;
  medium: string;
  strong: string;
}

export interface Breakpoints {
  xs: number;
  sm: number;
  md: number;
  lg: number;
  xl: number;
  '2xl': number;
}

export interface DesignTokens {
  colors: ColorPalette;
  typography: TypographyScale;
  spacing: SpacingSystem;
  borderRadius: BorderRadius;
  boxShadow: BoxShadow;
  breakpoints: Breakpoints;
}

// Animation types
export interface AnimationConfig {
  duration: {
    fast: string;
    normal: string;
    slow: string;
  };
  easing: {
    linear: string;
    easeIn: string;
    easeOut: string;
    easeInOut: string;
  };
  keyframes: Record<string, Record<string, any>>;
}

// Theme configuration
export interface ThemeMode {
  mode: 'light' | 'dark' | 'system';
  colors: Partial<ColorPalette>;
  isDark: boolean;
}

export interface DesignSystemConfig {
  tokens: DesignTokens;
  theme: ThemeMode;
  animation: AnimationConfig;
}