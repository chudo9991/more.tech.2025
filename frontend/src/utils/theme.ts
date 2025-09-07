// Theme utility functions for managing light/dark theme switching

export type Theme = 'light' | 'dark' | 'system';

export interface ThemeConfig {
  theme: Theme;
  systemPreference: 'light' | 'dark';
}

/**
 * Get the current system color scheme preference
 */
export function getSystemTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light';
  
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * Get the effective theme (resolves 'system' to actual theme)
 */
export function getEffectiveTheme(theme: Theme): 'light' | 'dark' {
  if (theme === 'system') {
    return getSystemTheme();
  }
  return theme;
}

/**
 * Apply theme to the document
 */
export function applyTheme(theme: Theme): void {
  const effectiveTheme = getEffectiveTheme(theme);
  const root = document.documentElement;
  
  // Remove existing theme attributes
  root.removeAttribute('data-theme');
  
  // Apply new theme
  if (effectiveTheme === 'dark') {
    root.setAttribute('data-theme', 'dark');
  }
  // Light theme is the default, no attribute needed
}

/**
 * Get stored theme preference from localStorage
 */
export function getStoredTheme(): Theme {
  if (typeof window === 'undefined') return 'system';
  
  try {
    const stored = localStorage.getItem('theme') as Theme;
    if (stored && ['light', 'dark', 'system'].includes(stored)) {
      return stored;
    }
  } catch (error) {
    console.warn('Failed to read theme from localStorage:', error);
  }
  
  return 'system';
}

/**
 * Store theme preference in localStorage
 */
export function setStoredTheme(theme: Theme): void {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem('theme', theme);
  } catch (error) {
    console.warn('Failed to store theme in localStorage:', error);
  }
}

/**
 * Initialize theme system
 */
export function initializeTheme(): Theme {
  const storedTheme = getStoredTheme();
  applyTheme(storedTheme);
  return storedTheme;
}

/**
 * Set up system theme change listener
 */
export function setupSystemThemeListener(callback: (theme: 'light' | 'dark') => void): () => void {
  if (typeof window === 'undefined') return () => {};
  
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  
  const handleChange = (e: MediaQueryListEvent) => {
    callback(e.matches ? 'dark' : 'light');
  };
  
  mediaQuery.addEventListener('change', handleChange);
  
  // Return cleanup function
  return () => {
    mediaQuery.removeEventListener('change', handleChange);
  };
}

/**
 * Toggle between light and dark themes
 */
export function toggleTheme(currentTheme: Theme): Theme {
  const effectiveTheme = getEffectiveTheme(currentTheme);
  const newTheme: Theme = effectiveTheme === 'light' ? 'dark' : 'light';
  
  applyTheme(newTheme);
  setStoredTheme(newTheme);
  
  return newTheme;
}

/**
 * Set specific theme
 */
export function setTheme(theme: Theme): void {
  applyTheme(theme);
  setStoredTheme(theme);
}

/**
 * Get theme configuration object
 */
export function getThemeConfig(): ThemeConfig {
  return {
    theme: getStoredTheme(),
    systemPreference: getSystemTheme(),
  };
}