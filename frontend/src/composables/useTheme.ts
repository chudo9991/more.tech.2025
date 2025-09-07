// Vue composable for theme management

import { ref, computed, watch } from 'vue';
import type { Theme } from '@/utils/theme';
import {
  getStoredTheme,
  getSystemTheme,
  getEffectiveTheme,
  applyTheme,
  setStoredTheme,
  setupSystemThemeListener,
  toggleTheme as utilToggleTheme,
  setTheme as utilSetTheme,
} from '@/utils/theme';

export function useTheme() {
  // Reactive state
  const currentTheme = ref<Theme>('system');
  const systemTheme = ref<'light' | 'dark'>('light');
  
  // Computed properties
  const effectiveTheme = computed(() => getEffectiveTheme(currentTheme.value));
  const isDark = computed(() => effectiveTheme.value === 'dark');
  const isLight = computed(() => effectiveTheme.value === 'light');
  
  // Theme options for UI
  const themeOptions = [
    { value: 'light' as const, label: 'Light', icon: '☀️' },
    { value: 'dark' as const, label: 'Dark', icon: '🌙' },
    { value: 'system' as const, label: 'System', icon: '💻' },
  ];
  
  // System theme listener cleanup function
  let cleanupSystemListener: (() => void) | null = null;
  
  // Initialize theme
  const initTheme = () => {
    currentTheme.value = getStoredTheme();
    systemTheme.value = getSystemTheme();
    applyTheme(currentTheme.value);
  };
  
  // Set theme
  const setTheme = (theme: Theme) => {
    currentTheme.value = theme;
    utilSetTheme(theme);
  };
  
  // Toggle between light and dark
  const toggleTheme = () => {
    const newTheme = utilToggleTheme(currentTheme.value);
    currentTheme.value = newTheme;
  };
  
  // Update system theme when it changes
  const updateSystemTheme = (newSystemTheme: 'light' | 'dark') => {
    systemTheme.value = newSystemTheme;
    
    // If current theme is 'system', reapply to reflect the change
    if (currentTheme.value === 'system') {
      applyTheme('system');
    }
  };
  
  // Watch for theme changes and apply them
  watch(currentTheme, (newTheme) => {
    applyTheme(newTheme);
    setStoredTheme(newTheme);
  });
  
  // Initialize on first use
  initTheme();
  
  // Set up system theme change listener
  cleanupSystemListener = setupSystemThemeListener(updateSystemTheme);
  
  return {
    // State
    currentTheme,
    systemTheme,
    effectiveTheme,
    isDark,
    isLight,
    themeOptions,
    
    // Actions
    setTheme,
    toggleTheme,
    initTheme,
  };
}

// Export types for external use
export type { Theme };