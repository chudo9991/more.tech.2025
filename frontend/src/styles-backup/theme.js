// ===== THEME MANAGEMENT UTILITIES =====

// Theme utility functions for managing light/dark theme switching
export function getSystemTheme() {
  if (typeof window === 'undefined') return 'light';
  
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function getEffectiveTheme(theme) {
  if (theme === 'system') {
    return getSystemTheme();
  }
  return theme;
}

export function applyTheme(theme) {
  const effectiveTheme = getEffectiveTheme(theme);
  const root = document.documentElement;
  
  // Remove existing theme attributes
  root.removeAttribute('data-theme');
  
  // Apply new theme
  if (effectiveTheme === 'dark') {
    root.setAttribute('data-theme', 'dark');
    // Apply glassmorphism dark theme
    applyGlassmorphismTheme();
    // Apply Element Plus theme overrides
    applyElementPlusTheme();
  } else {
    // Light theme - remove glassmorphism specific styles
    removeGlassmorphismTheme();
  }
}

// Apply glassmorphism theme variables to document
export function applyGlassmorphismTheme() {
  const root = document.documentElement;
  const overrides = getElementPlusThemeOverrides();
  
  // Apply Element Plus CSS variables
  Object.entries(overrides).forEach(([property, value]) => {
    root.style.setProperty(property, value);
  });
  
  // Ensure body has proper background for glassmorphism
  document.body.style.background = 'var(--gradient-dark)';
  document.body.style.minHeight = '100vh';
}

// Remove glassmorphism theme variables
export function removeGlassmorphismTheme() {
  const root = document.documentElement;
  const overrides = getElementPlusThemeOverrides();
  
  // Remove Element Plus CSS variables
  Object.keys(overrides).forEach((property) => {
    root.style.removeProperty(property);
  });
  
  // Reset body background
  document.body.style.background = '';
  document.body.style.minHeight = '';
}

// Apply Element Plus theme specifically
export function applyElementPlusTheme() {
  // This function can be extended to apply additional Element Plus specific theming
  // For now, it's handled in applyGlassmorphismTheme
}

export function getStoredTheme() {
  if (typeof window === 'undefined') return 'system';
  
  try {
    const stored = localStorage.getItem('theme');
    if (stored && ['light', 'dark', 'system'].includes(stored)) {
      return stored;
    }
  } catch (error) {
    console.warn('Failed to read theme from localStorage:', error);
  }
  
  return 'system';
}

export function setStoredTheme(theme) {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem('theme', theme);
  } catch (error) {
    console.warn('Failed to store theme in localStorage:', error);
  }
}

export function initializeTheme() {
  const storedTheme = getStoredTheme();
  applyTheme(storedTheme);
  
  // Always apply glassmorphism theme for dark mode
  const effectiveTheme = getEffectiveTheme(storedTheme);
  if (effectiveTheme === 'dark') {
    applyGlassmorphismTheme();
  }
  
  return storedTheme;
}

// Auto-initialize glassmorphism theme
export function autoInitializeGlassmorphismTheme() {
  // Force dark theme for glassmorphism experience
  const root = document.documentElement;
  root.setAttribute('data-theme', 'dark');
  
  // Apply glassmorphism theme
  applyGlassmorphismTheme();
  
  // Store dark theme preference
  setStoredTheme('dark');
  
  return 'dark';
}

export function setupSystemThemeListener(callback) {
  if (typeof window === 'undefined') return () => {};
  
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  
  const handleChange = (e) => {
    callback(e.matches ? 'dark' : 'light');
  };
  
  mediaQuery.addEventListener('change', handleChange);
  
  // Return cleanup function
  return () => {
    mediaQuery.removeEventListener('change', handleChange);
  };
}

export function toggleTheme(currentTheme) {
  const effectiveTheme = getEffectiveTheme(currentTheme);
  const newTheme = effectiveTheme === 'light' ? 'dark' : 'light';
  
  applyTheme(newTheme);
  setStoredTheme(newTheme);
  
  return newTheme;
}

export function setTheme(theme) {
  applyTheme(theme);
  setStoredTheme(theme);
}

export function getThemeConfig() {
  return {
    theme: getStoredTheme(),
    systemPreference: getSystemTheme(),
  };
}

// ===== GLASSMORPHISM & DARK THEME CONFIGURATION =====

export const glassmorphismTheme = {
  // CSS Variables for JavaScript usage
  variables: {
    // Dark Theme Colors
    darkBgPrimary: '#0f0f23',
    darkBgSecondary: '#1a1a2e',
    darkBgTertiary: '#16213e',
    darkTextPrimary: '#ffffff',
    darkTextSecondary: 'rgba(255, 255, 255, 0.8)',
    darkTextMuted: 'rgba(255, 255, 255, 0.6)',
    
    // Glassmorphism Effects
    glassBgLight: 'rgba(255, 255, 255, 0.1)',
    glassBgMedium: 'rgba(255, 255, 255, 0.15)',
    glassBgStrong: 'rgba(255, 255, 255, 0.2)',
    glassBgSubtle: 'rgba(255, 255, 255, 0.05)',
    
    glassBorderLight: 'rgba(255, 255, 255, 0.1)',
    glassBorderMedium: 'rgba(255, 255, 255, 0.2)',
    glassBorderStrong: 'rgba(255, 255, 255, 0.3)',
    
    // Gradients
    gradientPrimary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    gradientSecondary: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    gradientSuccess: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
    gradientWarning: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    gradientDanger: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)',
    gradientDark: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%)',
    
    // Shadows
    glassShadowLight: '0 8px 32px rgba(31, 38, 135, 0.37)',
    glassShadowMedium: '0 8px 32px rgba(31, 38, 135, 0.5)',
    glassShadowStrong: '0 12px 40px rgba(31, 38, 135, 0.6)',
    glassShadowGlow: '0 0 20px rgba(255, 255, 255, 0.1)',
    
    // Animation
    animationDurationFast: '0.15s',
    animationDurationNormal: '0.3s',
    animationDurationSlow: '0.5s',
    animationEasing: 'cubic-bezier(0.4, 0, 0.2, 1)',
    animationEasingBounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
  },
  
  // Glassmorphism Style Generators
  glass: {
    subtle: {
      background: 'rgba(255, 255, 255, 0.05)',
      backdropFilter: 'blur(3px)',
      WebkitBackdropFilter: 'blur(3px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: '0 8px 32px rgba(31, 38, 135, 0.2)'
    },
    light: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      boxShadow: '0 8px 32px rgba(31, 38, 135, 0.37)'
    },
    medium: {
      background: 'rgba(255, 255, 255, 0.15)',
      backdropFilter: 'blur(15px)',
      WebkitBackdropFilter: 'blur(15px)',
      border: '1px solid rgba(255, 255, 255, 0.25)',
      boxShadow: '0 8px 32px rgba(31, 38, 135, 0.5)'
    },
    strong: {
      background: 'rgba(255, 255, 255, 0.2)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.3)',
      boxShadow: '0 12px 40px rgba(31, 38, 135, 0.6)'
    },
    glow: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      boxShadow: '0 0 20px rgba(255, 255, 255, 0.1), 0 8px 32px rgba(31, 38, 135, 0.37)'
    }
  },
  
  // Animation Presets
  animations: {
    fadeIn: {
      animation: 'fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
    },
    fadeInFast: {
      animation: 'fadeIn 0.15s cubic-bezier(0.4, 0, 0.2, 1)'
    },
    slideUp: {
      animation: 'slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
    },
    slideDown: {
      animation: 'slideDown 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
    },
    scaleIn: {
      animation: 'scaleIn 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)'
    },
    bounceIn: {
      animation: 'bounceIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)'
    },
    pulseGlow: {
      animation: 'pulseGlow 2s ease-in-out infinite'
    },
    float: {
      animation: 'float 3s ease-in-out infinite'
    },
    shimmer: {
      animation: 'shimmer 2s linear infinite',
      background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent)',
      backgroundSize: '200% 100%'
    }
  },
  
  // Hover Effects
  hoverEffects: {
    lift: {
      transition: 'all 0.3s ease',
      ':hover': {
        transform: 'translateY(-4px)',
        boxShadow: '0 12px 50px rgba(0, 0, 0, 0.25)'
      }
    },
    glow: {
      transition: 'all 0.3s ease',
      ':hover': {
        boxShadow: '0 0 20px rgba(255, 255, 255, 0.3)'
      }
    },
    scale: {
      transition: 'transform 0.3s ease',
      ':hover': {
        transform: 'scale(1.05)'
      }
    }
  },
  
  // Component Presets
  components: {
    button: {
      base: {
        ...this?.glass?.light,
        padding: '12px 24px',
        borderRadius: '8px',
        fontWeight: '500',
        color: '#ffffff',
        cursor: 'pointer',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        position: 'relative',
        overflow: 'hidden'
      },
      primary: {
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      },
      success: {
        background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'
      },
      warning: {
        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
      },
      danger: {
        background: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)'
      }
    },
    card: {
      base: {
        ...this?.glass?.light,
        padding: '24px',
        borderRadius: '16px',
        color: '#ffffff',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
      },
      hover: {
        cursor: 'pointer',
        ':hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 50px rgba(0, 0, 0, 0.25)'
        }
      }
    },
    input: {
      base: {
        background: 'rgba(255, 255, 255, 0.05)',
        backdropFilter: 'blur(5px)',
        WebkitBackdropFilter: 'blur(5px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '12px 16px',
        borderRadius: '8px',
        color: '#ffffff',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '::placeholder': {
          color: 'rgba(255, 255, 255, 0.6)'
        },
        ':focus': {
          background: 'rgba(255, 255, 255, 0.15)',
          borderColor: 'rgba(255, 255, 255, 0.25)',
          boxShadow: '0 0 0 2px rgba(255, 255, 255, 0.1)',
          outline: 'none'
        }
      }
    },
    modal: {
      backdrop: {
        background: 'rgba(0, 0, 0, 0.5)',
        backdropFilter: 'blur(5px)',
        WebkitBackdropFilter: 'blur(5px)'
      },
      container: {
        ...this?.glass?.strong,
        padding: '32px',
        borderRadius: '20px',
        color: '#ffffff',
        maxWidth: '90vw',
        maxHeight: '90vh',
        overflowY: 'auto'
      }
    }
  }
};

// Utility Functions
export const applyGlassmorphism = (variant = 'light') => {
  return glassmorphismTheme.glass[variant] || glassmorphismTheme.glass.light;
};

export const applyAnimation = (animationType) => {
  return glassmorphismTheme.animations[animationType] || {};
};

export const applyHoverEffect = (effectType) => {
  return glassmorphismTheme.hoverEffects[effectType] || {};
};

export const getComponentStyle = (component, variant = 'base') => {
  const componentStyles = glassmorphismTheme.components[component];
  if (!componentStyles) return {};
  
  return {
    ...componentStyles.base,
    ...(componentStyles[variant] || {})
  };
};

// CSS-in-JS Helper
export const createGlassStyle = (options = {}) => {
  const {
    opacity = 0.1,
    blur = 10,
    borderOpacity = 0.2,
    shadow = 'light'
  } = options;
  
  return {
    background: `rgba(255, 255, 255, ${opacity})`,
    backdropFilter: `blur(${blur}px)`,
    WebkitBackdropFilter: `blur(${blur}px)`,
    border: `1px solid rgba(255, 255, 255, ${borderOpacity})`,
    boxShadow: glassmorphismTheme.variables[`glassShadow${shadow.charAt(0).toUpperCase() + shadow.slice(1)}`]
  };
};

// Element Plus Theme Integration Helper
export const getElementPlusThemeOverrides = () => {
  return {
    // Primary Colors - Glassmorphism Neon Cyan
    '--el-color-primary': '#00ffff',
    '--el-color-primary-light-3': 'rgba(0, 255, 255, 0.7)',
    '--el-color-primary-light-5': 'rgba(0, 255, 255, 0.5)',
    '--el-color-primary-light-7': 'rgba(0, 255, 255, 0.3)',
    '--el-color-primary-light-8': 'rgba(0, 255, 255, 0.2)',
    '--el-color-primary-light-9': 'rgba(0, 255, 255, 0.1)',
    '--el-color-primary-dark-2': '#00e6e6',
    
    // Success Colors - Neon Green
    '--el-color-success': '#10b981',
    '--el-color-success-light-3': 'rgba(16, 185, 129, 0.7)',
    '--el-color-success-light-5': 'rgba(16, 185, 129, 0.5)',
    '--el-color-success-light-7': 'rgba(16, 185, 129, 0.3)',
    '--el-color-success-light-8': 'rgba(16, 185, 129, 0.2)',
    '--el-color-success-light-9': 'rgba(16, 185, 129, 0.1)',
    
    // Warning Colors - Neon Orange
    '--el-color-warning': '#f59e0b',
    '--el-color-warning-light-3': 'rgba(245, 158, 11, 0.7)',
    '--el-color-warning-light-5': 'rgba(245, 158, 11, 0.5)',
    '--el-color-warning-light-7': 'rgba(245, 158, 11, 0.3)',
    '--el-color-warning-light-8': 'rgba(245, 158, 11, 0.2)',
    '--el-color-warning-light-9': 'rgba(245, 158, 11, 0.1)',
    
    // Error Colors - Neon Red
    '--el-color-error': '#ef4444',
    '--el-color-error-light-3': 'rgba(239, 68, 68, 0.7)',
    '--el-color-error-light-5': 'rgba(239, 68, 68, 0.5)',
    '--el-color-error-light-7': 'rgba(239, 68, 68, 0.3)',
    '--el-color-error-light-8': 'rgba(239, 68, 68, 0.2)',
    '--el-color-error-light-9': 'rgba(239, 68, 68, 0.1)',
    
    // Background Colors - Glassmorphism
    '--el-bg-color': 'rgba(255, 255, 255, 0.1)',
    '--el-bg-color-page': 'transparent',
    '--el-bg-color-overlay': 'rgba(0, 0, 0, 0.5)',
    
    // Text Colors - Dark Theme
    '--el-text-color-primary': '#ffffff',
    '--el-text-color-regular': 'rgba(255, 255, 255, 0.8)',
    '--el-text-color-secondary': 'rgba(255, 255, 255, 0.6)',
    '--el-text-color-placeholder': 'rgba(255, 255, 255, 0.4)',
    '--el-text-color-disabled': 'rgba(255, 255, 255, 0.3)',
    
    // Border Colors - Glassmorphism
    '--el-border-color': 'rgba(255, 255, 255, 0.2)',
    '--el-border-color-light': 'rgba(255, 255, 255, 0.1)',
    '--el-border-color-lighter': 'rgba(255, 255, 255, 0.05)',
    '--el-border-color-extra-light': 'rgba(255, 255, 255, 0.02)',
    '--el-border-color-dark': 'rgba(255, 255, 255, 0.3)',
    '--el-border-color-darker': 'rgba(255, 255, 255, 0.4)',
    
    // Fill Colors - Glassmorphism
    '--el-fill-color': 'rgba(255, 255, 255, 0.1)',
    '--el-fill-color-light': 'rgba(255, 255, 255, 0.05)',
    '--el-fill-color-lighter': 'rgba(255, 255, 255, 0.02)',
    '--el-fill-color-extra-light': 'rgba(255, 255, 255, 0.01)',
    '--el-fill-color-dark': 'rgba(255, 255, 255, 0.15)',
    '--el-fill-color-darker': 'rgba(255, 255, 255, 0.2)',
    '--el-fill-color-blank': 'transparent',
    
    // Box Shadows - Glassmorphism
    '--el-box-shadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
    '--el-box-shadow-light': '0 8px 32px rgba(31, 38, 135, 0.2)',
    '--el-box-shadow-base': '0 8px 32px rgba(31, 38, 135, 0.37)',
    '--el-box-shadow-dark': '0 12px 40px rgba(31, 38, 135, 0.6)',
    
    // Mask Colors
    '--el-mask-color': 'rgba(0, 0, 0, 0.5)',
    '--el-mask-color-extra-light': 'rgba(0, 0, 0, 0.3)',
    
    // Component Specific Overrides
    '--el-component-size-large': '40px',
    '--el-component-size': '32px',
    '--el-component-size-small': '24px',
    
    // Border Radius
    '--el-border-radius-base': '8px',
    '--el-border-radius-small': '4px',
    '--el-border-radius-round': '20px',
    '--el-border-radius-circle': '100%',
    
    // Transition
    '--el-transition-duration': '0.3s',
    '--el-transition-duration-fast': '0.15s',
    '--el-transition-function-ease-in-out-bezier': 'cubic-bezier(0.4, 0, 0.2, 1)',
    '--el-transition-function-fast-bezier': 'cubic-bezier(0.23, 1, 0.32, 1)',
    
    // Font
    '--el-font-size-extra-large': '20px',
    '--el-font-size-large': '18px',
    '--el-font-size-medium': '16px',
    '--el-font-size-base': '14px',
    '--el-font-size-small': '13px',
    '--el-font-size-extra-small': '12px',
    
    // Z-index
    '--el-index-normal': '1',
    '--el-index-top': '1000',
    '--el-index-popper': '2000'
  };
};

// Enhanced Element Plus Component Overrides
export const getElementPlusComponentOverrides = () => {
  return {
    // Button overrides
    button: {
      '--el-button-bg-color': 'var(--glass-bg-light)',
      '--el-button-border-color': 'var(--glass-border-medium)',
      '--el-button-hover-bg-color': 'var(--glass-bg-medium)',
      '--el-button-hover-border-color': 'var(--glass-border-strong)',
      '--el-button-active-bg-color': 'var(--glass-bg-strong)',
      '--el-button-active-border-color': 'var(--glass-border-strong)'
    },
    
    // Input overrides
    input: {
      '--el-input-bg-color': 'var(--glass-bg-subtle)',
      '--el-input-border-color': 'var(--glass-border-light)',
      '--el-input-hover-border-color': 'var(--glass-border-medium)',
      '--el-input-focus-border-color': 'var(--neon-cyan)',
      '--el-input-text-color': 'var(--dark-text-primary)',
      '--el-input-placeholder-color': 'var(--dark-text-muted)'
    },
    
    // Card overrides
    card: {
      '--el-card-bg-color': 'var(--glass-bg-light)',
      '--el-card-border-color': 'var(--glass-border-medium)',
      '--el-card-shadow': 'var(--glass-shadow-light)'
    },
    
    // Table overrides
    table: {
      '--el-table-bg-color': 'var(--glass-bg-subtle)',
      '--el-table-tr-bg-color': 'transparent',
      '--el-table-header-bg-color': 'var(--glass-bg-light)',
      '--el-table-row-hover-bg-color': 'var(--glass-bg-light)',
      '--el-table-border-color': 'var(--glass-border-light)',
      '--el-table-text-color': 'var(--dark-text-primary)',
      '--el-table-header-text-color': 'var(--dark-text-primary)'
    },
    
    // Dialog overrides
    dialog: {
      '--el-dialog-bg-color': 'var(--glass-bg-medium)',
      '--el-dialog-border-color': 'var(--glass-border-medium)',
      '--el-dialog-shadow': 'var(--glass-shadow-strong)',
      '--el-dialog-title-font-size': '18px',
      '--el-dialog-content-font-size': '14px'
    },
    
    // Dropdown overrides
    dropdown: {
      '--el-dropdown-bg-color': 'var(--glass-bg-medium)',
      '--el-dropdown-border-color': 'var(--glass-border-medium)',
      '--el-dropdown-shadow': 'var(--glass-shadow-medium)'
    },
    
    // Pagination overrides
    pagination: {
      '--el-pagination-bg-color': 'var(--glass-bg-subtle)',
      '--el-pagination-hover-color': 'var(--neon-cyan)',
      '--el-pagination-button-bg-color': 'var(--glass-bg-light)',
      '--el-pagination-button-border-color': 'var(--glass-border-light)'
    }
  };
};

export default glassmorphismTheme;