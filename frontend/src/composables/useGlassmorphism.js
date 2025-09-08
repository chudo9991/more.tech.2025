// ===== GLASSMORPHISM THEME COMPOSABLE =====

import { ref, computed, onMounted } from 'vue';
import { 
  glassmorphismTheme, 
  applyGlassmorphism, 
  applyAnimation, 
  applyHoverEffect,
  getComponentStyle,
  createGlassStyle,
  getElementPlusThemeOverrides
} from '@/styles/theme.js';

export function useGlassmorphism() {
  // Reactive theme state
  const isThemeLoaded = ref(false);
  const currentVariant = ref('light');
  
  // Apply CSS variables to document root
  const applyThemeVariables = () => {
    const root = document.documentElement;
    const variables = glassmorphismTheme.variables;
    
    Object.entries(variables).forEach(([key, value]) => {
      const cssVar = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
      root.style.setProperty(cssVar, value);
    });
    
    // Apply Element Plus theme overrides
    const elementPlusOverrides = getElementPlusThemeOverrides();
    Object.entries(elementPlusOverrides).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
    
    isThemeLoaded.value = true;
  };
  
  // Glassmorphism style generators
  const glass = computed(() => ({
    subtle: applyGlassmorphism('subtle'),
    light: applyGlassmorphism('light'),
    medium: applyGlassmorphism('medium'),
    strong: applyGlassmorphism('strong'),
    glow: applyGlassmorphism('glow')
  }));
  
  // Animation helpers
  const animations = computed(() => ({
    fadeIn: applyAnimation('fadeIn'),
    fadeInFast: applyAnimation('fadeInFast'),
    slideUp: applyAnimation('slideUp'),
    slideDown: applyAnimation('slideDown'),
    scaleIn: applyAnimation('scaleIn'),
    bounceIn: applyAnimation('bounceIn'),
    pulseGlow: applyAnimation('pulseGlow'),
    float: applyAnimation('float'),
    shimmer: applyAnimation('shimmer')
  }));
  
  // Hover effects
  const hoverEffects = computed(() => ({
    lift: applyHoverEffect('lift'),
    glow: applyHoverEffect('glow'),
    scale: applyHoverEffect('scale')
  }));
  
  // Component style generators
  const getButtonStyle = (variant = 'base') => {
    return getComponentStyle('button', variant);
  };
  
  const getCardStyle = (variant = 'base') => {
    return getComponentStyle('card', variant);
  };
  
  const getInputStyle = () => {
    return getComponentStyle('input', 'base');
  };
  
  const getModalStyle = (part = 'container') => {
    const modalStyles = glassmorphismTheme.components.modal;
    return modalStyles[part] || modalStyles.container;
  };
  
  // Custom glass style creator
  const createCustomGlass = (options) => {
    return createGlassStyle(options);
  };
  
  // Gradient generators
  const gradients = computed(() => ({
    primary: glassmorphismTheme.variables.gradientPrimary,
    secondary: glassmorphismTheme.variables.gradientSecondary,
    success: glassmorphismTheme.variables.gradientSuccess,
    warning: glassmorphismTheme.variables.gradientWarning,
    danger: glassmorphismTheme.variables.gradientDanger,
    dark: glassmorphismTheme.variables.gradientDark
  }));
  
  // CSS class generators for template usage
  const getGlassClasses = (variant = 'light') => {
    const baseClasses = 'transition-all duration-300';
    const variantClasses = {
      subtle: 'glass-subtle',
      light: 'glass',
      medium: 'glass-medium',
      strong: 'glass-strong',
      glow: 'glass-glow'
    };
    
    return `${baseClasses} ${variantClasses[variant] || variantClasses.light}`;
  };
  
  const getAnimationClasses = (animation) => {
    const animationClasses = {
      fadeIn: 'animate-fade-in',
      fadeInFast: 'animate-fade-in-fast',
      slideUp: 'animate-slide-up',
      slideDown: 'animate-slide-down',
      scaleIn: 'animate-scale-in',
      bounceIn: 'animate-bounce-in',
      pulseGlow: 'animate-pulse-glow',
      float: 'animate-float',
      shimmer: 'animate-shimmer'
    };
    
    return animationClasses[animation] || '';
  };
  
  const getHoverClasses = (effect) => {
    const hoverClasses = {
      lift: 'hover-lift',
      glow: 'hover-glow',
      scale: 'hover-scale'
    };
    
    return hoverClasses[effect] || '';
  };
  
  const getRippleClasses = (variant = 'default') => {
    const rippleClasses = {
      default: 'ripple',
      primary: 'ripple ripple-primary',
      success: 'ripple ripple-success',
      warning: 'ripple ripple-warning',
      danger: 'ripple ripple-danger',
      subtle: 'ripple ripple-subtle',
      strong: 'ripple ripple-strong'
    };
    
    return rippleClasses[variant] || rippleClasses.default;
  };
  
  // Utility functions
  const combineClasses = (...classes) => {
    return classes.filter(Boolean).join(' ');
  };
  
  const createButtonClasses = (variant = 'primary', size = 'medium', effects = []) => {
    const baseClasses = getGlassClasses('light');
    const rippleClasses = getRippleClasses(variant);
    const hoverClasses = getHoverClasses('lift');
    const effectClasses = effects.map(effect => getAnimationClasses(effect)).join(' ');
    
    const sizeClasses = {
      small: 'px-3 py-2 text-sm',
      medium: 'px-6 py-3 text-base',
      large: 'px-8 py-4 text-lg'
    };
    
    const variantClasses = {
      primary: 'bg-gradient-primary',
      secondary: 'bg-gradient-secondary',
      success: 'bg-gradient-success',
      warning: 'bg-gradient-warning',
      danger: 'bg-gradient-danger'
    };
    
    return combineClasses(
      baseClasses,
      rippleClasses,
      hoverClasses,
      sizeClasses[size] || sizeClasses.medium,
      variantClasses[variant] || variantClasses.primary,
      effectClasses,
      'rounded-lg font-medium cursor-pointer'
    );
  };
  
  const createCardClasses = (variant = 'base', effects = []) => {
    const baseClasses = getGlassClasses('light');
    const hoverClasses = variant === 'hover' ? getHoverClasses('lift') : '';
    const rippleClasses = variant === 'hover' ? getRippleClasses() : '';
    const effectClasses = effects.map(effect => getAnimationClasses(effect)).join(' ');
    
    return combineClasses(
      baseClasses,
      hoverClasses,
      rippleClasses,
      effectClasses,
      'rounded-xl p-6'
    );
  };
  
  // Theme utilities
  const setThemeVariant = (variant) => {
    currentVariant.value = variant;
  };
  
  const getThemeVariant = () => {
    return currentVariant.value;
  };
  
  // Initialize theme on mount
  onMounted(() => {
    applyThemeVariables();
  });
  
  return {
    // State
    isThemeLoaded,
    currentVariant,
    
    // Style objects
    glass,
    animations,
    hoverEffects,
    gradients,
    
    // Style generators
    getButtonStyle,
    getCardStyle,
    getInputStyle,
    getModalStyle,
    createCustomGlass,
    
    // CSS class generators
    getGlassClasses,
    getAnimationClasses,
    getHoverClasses,
    getRippleClasses,
    createButtonClasses,
    createCardClasses,
    
    // Utilities
    combineClasses,
    applyThemeVariables,
    setThemeVariant,
    getThemeVariant,
    
    // Theme data
    theme: glassmorphismTheme
  };
}

// Export for direct usage without composable
export {
  glassmorphismTheme,
  applyGlassmorphism,
  applyAnimation,
  applyHoverEffect,
  getComponentStyle,
  createGlassStyle,
  getElementPlusThemeOverrides
};