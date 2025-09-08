# Glassmorphism & Dark Theme System

This document describes how to use the comprehensive glassmorphism and dark theme system implemented in the frontend.

## Overview

The system provides:
- **Dark theme with glassmorphism effects**
- **Comprehensive CSS utilities and SCSS mixins**
- **Vue composables for easy integration**
- **Element Plus theme integration**
- **Animation and hover effects**
- **Responsive design support**

## Quick Start

### 1. Using CSS Classes (Recommended for most cases)

```vue
<template>
  <!-- Glassmorphism button -->
  <button class="btn-glass-primary ripple hover-lift">
    Click me
  </button>
  
  <!-- Glassmorphism card -->
  <div class="card-glass hover-lift animate-fade-in">
    <h3>Card Title</h3>
    <p>Card content</p>
  </div>
  
  <!-- Glassmorphism input -->
  <input class="input-glass" placeholder="Enter text..." />
</template>
```

### 2. Using Vue Composable

```vue
<template>
  <div :class="createCardClasses('hover', ['fadeIn'])">
    <button :class="createButtonClasses('primary', 'medium', ['pulseGlow'])">
      Dynamic Button
    </button>
  </div>
</template>

<script setup>
import { useGlassmorphism } from '@/composables/useGlassmorphism.js'

const { createCardClasses, createButtonClasses } = useGlassmorphism()
</script>
```

### 3. Using SCSS Mixins

```vue
<template>
  <div class="my-custom-component">
    <button class="my-button">Custom Button</button>
  </div>
</template>

<style lang="scss" scoped>
@import '@/styles/mixins';

.my-custom-component {
  @include card-glass();
  @include fade-in();
}

.my-button {
  @include btn-glass-primary();
  @include hover-lift();
}
</style>
```

## Available CSS Classes

### Glassmorphism Effects
- `glass` - Standard glassmorphism effect
- `glass-subtle` - Subtle glassmorphism (less opacity)
- `glass-medium` - Medium glassmorphism
- `glass-strong` - Strong glassmorphism (more opacity)
- `glass-glow` - Glassmorphism with glow effect

### Gradient Backgrounds
- `bg-gradient-primary` - Primary gradient (purple-blue)
- `bg-gradient-secondary` - Secondary gradient (blue-cyan)
- `bg-gradient-success` - Success gradient (teal-green)
- `bg-gradient-warning` - Warning gradient (pink-red)
- `bg-gradient-danger` - Danger gradient (red-orange)
- `bg-gradient-animated` - Animated shifting gradient

### Animations
- `animate-fade-in` - Fade in animation
- `animate-fade-in-fast` - Fast fade in
- `animate-slide-up` - Slide up animation
- `animate-slide-down` - Slide down animation
- `animate-slide-left` - Slide left animation
- `animate-slide-right` - Slide right animation
- `animate-scale-in` - Scale in with bounce
- `animate-bounce-in` - Bounce in animation
- `animate-pulse-glow` - Pulsing glow effect
- `animate-float` - Floating animation
- `animate-shimmer` - Shimmer loading effect

### Hover Effects
- `hover-lift` - Lift on hover with shadow
- `hover-glow` - Glow effect on hover
- `hover-scale` - Scale up on hover

### Ripple Effects
- `ripple` - Basic white ripple
- `ripple-primary` - Primary color ripple
- `ripple-success` - Success color ripple
- `ripple-warning` - Warning color ripple
- `ripple-danger` - Danger color ripple
- `ripple-subtle` - Subtle ripple effect
- `ripple-strong` - Strong ripple effect

### Component Classes
- `btn-glass` - Base glassmorphism button
- `btn-glass-primary` - Primary glassmorphism button
- `btn-glass-success` - Success glassmorphism button
- `btn-glass-warning` - Warning glassmorphism button
- `btn-glass-danger` - Danger glassmorphism button
- `card-glass` - Base glassmorphism card
- `card-glass-hover` - Hoverable glassmorphism card
- `input-glass` - Glassmorphism input field
- `modal-glass` - Glassmorphism modal container
- `nav-glass` - Glassmorphism navigation
- `badge-glass-*` - Glassmorphism badges (success, warning, danger, info)

## SCSS Mixins

### Glassmorphism Mixins
```scss
@include glassmorphism($opacity, $blur, $border-opacity);
@include glass-subtle();
@include glass-light();
@include glass-medium();
@include glass-strong();
```

### Gradient Mixins
```scss
@include gradient-primary();
@include gradient-secondary();
@include gradient-success();
@include gradient-warning();
@include gradient-danger();
@include gradient-animated();
```

### Animation Mixins
```scss
@include fade-in($duration, $easing);
@include slide-up($duration, $easing);
@include scale-in($duration, $easing);
@include bounce-in($duration);
@include pulse-glow($duration);
@include float($duration);
@include shimmer($duration);
```

### Component Mixins
```scss
@include btn-glass($padding, $border-radius);
@include btn-glass-primary();
@include card-glass($padding, $border-radius);
@include card-glass-hover();
@include input-glass($padding, $border-radius);
@include modal-glass($padding, $border-radius);
```

### Hover Effect Mixins
```scss
@include hover-lift($translate-y, $shadow);
@include hover-glow($glow-color);
@include hover-scale($scale);
@include ripple($color, $duration);
```

## Vue Composable API

### useGlassmorphism()

```javascript
const {
  // CSS class generators
  getGlassClasses,
  getAnimationClasses,
  getHoverClasses,
  getRippleClasses,
  createButtonClasses,
  createCardClasses,
  
  // Style objects for :style binding
  glass,
  animations,
  hoverEffects,
  gradients,
  
  // Component style generators
  getButtonStyle,
  getCardStyle,
  getInputStyle,
  getModalStyle,
  
  // Utilities
  combineClasses,
  createCustomGlass,
  
  // Theme management
  applyThemeVariables,
  setThemeVariant,
  getThemeVariant
} = useGlassmorphism()
```

### Examples

```javascript
// Generate button classes
const buttonClasses = createButtonClasses('primary', 'large', ['pulseGlow'])

// Generate card classes
const cardClasses = createCardClasses('hover', ['fadeIn', 'float'])

// Get style objects
const cardStyle = getCardStyle('hover')
const buttonStyle = getButtonStyle('primary')

// Create custom glassmorphism
const customGlass = createCustomGlass({
  opacity: 0.2,
  blur: 15,
  borderOpacity: 0.3,
  shadow: 'strong'
})
```

## Element Plus Integration

The system automatically applies glassmorphism styling to Element Plus components:

- **Buttons** - Glassmorphism background with gradients
- **Cards** - Transparent glassmorphism containers
- **Inputs** - Glassmorphism input fields with focus effects
- **Tables** - Transparent rows with hover effects
- **Dialogs** - Glassmorphism modals with backdrop blur
- **Select dropdowns** - Glassmorphism dropdown menus
- **Pagination** - Glassmorphism page buttons
- **Messages** - Glassmorphism notification messages

## CSS Variables

The system uses CSS variables that can be customized:

```css
:root {
  /* Dark Theme Colors */
  --dark-bg-primary: #0f0f23;
  --dark-text-primary: #ffffff;
  --dark-text-secondary: rgba(255, 255, 255, 0.8);
  
  /* Glassmorphism Effects */
  --glass-bg-light: rgba(255, 255, 255, 0.1);
  --glass-border-light: rgba(255, 255, 255, 0.1);
  --glass-blur-medium: blur(10px);
  
  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  /* Animation */
  --animation-duration-normal: 0.3s;
  --animation-easing: cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Browser Support

- **Modern browsers**: Full glassmorphism support with backdrop-filter
- **Older browsers**: Automatic fallback to solid backgrounds
- **Safari**: Full support with -webkit-backdrop-filter
- **Firefox**: Full support (backdrop-filter enabled by default in recent versions)

## Performance Considerations

- Glassmorphism effects use GPU acceleration
- Animations use transform and opacity for optimal performance
- Backdrop-filter is hardware accelerated on supported devices
- CSS variables allow for efficient theme switching

## Best Practices

1. **Use CSS classes for common patterns**
2. **Use SCSS mixins for custom components**
3. **Use Vue composable for dynamic styling**
4. **Combine effects sparingly to avoid visual overload**
5. **Test on different devices for performance**
6. **Use semantic color variants (primary, success, warning, danger)**

## Migration from Old Styles

To migrate existing components:

1. Replace solid backgrounds with glassmorphism classes
2. Add hover and animation effects
3. Update Element Plus components to use new theme
4. Test for visual consistency

## Examples

### Complete Component Example

```vue
<template>
  <div class="hr-panel">
    <!-- Header with glassmorphism -->
    <header class="nav-glass">
      <h1 class="text-2xl font-bold">HR Panel</h1>
      <button class="btn-glass-primary ripple">
        New Session
      </button>
    </header>
    
    <!-- Stats cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="card-glass hover-lift animate-fade-in">
        <div class="flex items-center">
          <div class="badge-glass-success">
            {{ stats.active }}
          </div>
          <span class="ml-3">Active Sessions</span>
        </div>
      </div>
    </div>
    
    <!-- Data table -->
    <div class="card-glass">
      <el-table :data="sessions" class="glassmorphism-table">
        <el-table-column prop="id" label="ID" />
        <el-table-column prop="status" label="Status">
          <template #default="{ row }">
            <span :class="getStatusBadgeClass(row.status)">
              {{ row.status }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { useGlassmorphism } from '@/composables/useGlassmorphism.js'

const { combineClasses } = useGlassmorphism()

const getStatusBadgeClass = (status) => {
  const baseClass = 'badge-glass'
  const statusClasses = {
    active: 'badge-glass-success',
    pending: 'badge-glass-warning',
    failed: 'badge-glass-danger'
  }
  return statusClasses[status] || baseClass
}
</script>

<style lang="scss" scoped>
@import '@/styles/mixins';

.hr-panel {
  @include fade-in();
  padding: 2rem;
}

.glassmorphism-table {
  :deep(.el-table__row:hover) {
    @include glass-light();
  }
}
</style>
```

This comprehensive system provides everything needed for a modern, glassmorphism-based dark theme interface while maintaining compatibility with Element Plus and providing multiple integration methods for different use cases.