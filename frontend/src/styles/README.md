# Design System Documentation

This document outlines the design system implementation for the modern UI redesign project.

## Overview

The design system is built using a combination of:
- **CSS Custom Properties** for theme-aware design tokens
- **TailwindCSS** for utility-first styling
- **Custom CSS utilities** for specialized layout and typography patterns

## Design Tokens

### Colors

#### Primary Colors
- Used for primary actions, links, and brand elements
- Available in shades 50-950
- CSS Variables: `--color-primary-50` to `--color-primary-950`

#### Neutral Colors
- Used for text, borders, and backgrounds
- Available in shades 50-950
- CSS Variables: `--color-neutral-50` to `--color-neutral-950`

#### Semantic Colors
- **Success**: Green tones for positive actions and states
- **Warning**: Orange/yellow tones for caution and warnings
- **Error**: Red tones for errors and destructive actions
- **Info**: Blue tones for informational content

#### Theme-Aware Colors
- `--color-background`: Main background color
- `--color-surface`: Card and component backgrounds
- `--color-surface-hover`: Hover state for surfaces
- `--color-text-primary`: Primary text color
- `--color-text-secondary`: Secondary text color
- `--color-text-muted`: Muted text color
- `--color-border`: Default border color
- `--color-border-hover`: Hover state for borders
- `--color-focus-ring`: Focus ring color

### Typography

#### Font Families
- **Sans**: `Inter, system-ui, sans-serif`
- **Mono**: `JetBrains Mono, monospace`

#### Font Sizes
- `xs`: 12px
- `sm`: 14px
- `base`: 16px
- `lg`: 18px
- `xl`: 20px
- `2xl`: 24px
- `3xl`: 30px
- `4xl`: 36px

#### Font Weights
- `normal`: 400
- `medium`: 500
- `semibold`: 600
- `bold`: 700

### Spacing

Based on a 4px grid system:
- `0`: 0px
- `1`: 4px
- `2`: 8px
- `3`: 12px
- `4`: 16px
- `6`: 24px
- `8`: 32px
- `12`: 48px
- `16`: 64px
- `20`: 80px

### Border Radius
- `sm`: 2px
- `base`: 4px
- `md`: 6px
- `lg`: 8px
- `xl`: 12px
- `2xl`: 16px
- `3xl`: 24px
- `full`: 9999px

### Shadows
- `soft`: Subtle shadow for cards
- `medium`: Medium shadow for elevated elements
- `strong`: Strong shadow for modals and overlays

## Theme System

### Light Theme (Default)
- Light backgrounds with dark text
- Subtle shadows and borders
- High contrast for accessibility

### Dark Theme
- Dark backgrounds with light text
- Adjusted shadows for dark surfaces
- Maintained contrast ratios

### System Theme
- Automatically follows user's system preference
- Switches between light and dark based on `prefers-color-scheme`

### Theme Implementation

```typescript
import { useTheme } from '@/composables/useTheme'

const { currentTheme, setTheme, toggleTheme, isDark } = useTheme()

// Set specific theme
setTheme('dark')

// Toggle between light and dark
toggleTheme()

// Check if dark theme is active
if (isDark.value) {
  // Dark theme specific logic
}
```

## Typography Utilities

### Display Typography
- `.text-display-1`: Large hero text
- `.text-display-2`: Secondary hero text
- `.text-display-fluid`: Responsive hero text

### Headings
- `.text-heading-1` to `.text-heading-4`: Semantic heading styles
- `.heading-section`: Section headings with spacing
- `.heading-subsection`: Subsection headings
- `.heading-card`: Card title headings

### Body Text
- `.text-body`: Standard body text
- `.text-body-large`: Large body text
- `.text-body-small`: Small body text
- `.text-paragraph`: Paragraph with proper spacing
- `.text-lead`: Lead paragraph text

### Specialized Text
- `.text-caption`: Small caption text
- `.text-code`: Inline code styling
- `.text-status`: Status badge text
- `.text-metric`: Large metric numbers

### Links
- `.link-primary`: Primary link styling
- `.link-secondary`: Secondary link styling

## Layout Utilities

### Containers
- `.container-xs` to `.container-xl`: Fixed-width containers
- `.container-responsive`: Responsive container with padding
- `.container-fluid`: Full-width container with padding

### Grid Layouts
- `.grid-responsive-2`: 1 column mobile, 2 columns tablet+
- `.grid-responsive-3`: 1 column mobile, 2 tablet, 3 desktop
- `.grid-responsive-4`: 1 column mobile, 2 tablet, 4 desktop
- `.card-grid`: Responsive card grid layout

### Flexbox Utilities
- `.flex-center`: Center items horizontally and vertically
- `.flex-between`: Space between with center alignment
- `.flex-col-center`: Column layout with center alignment

### Spacing
- `.stack-xs` to `.stack-xl`: Vertical spacing between children
- `.section-spacing`: Consistent section padding
- `.space-y-responsive`: Responsive vertical spacing

### Specialized Layouts
- `.layout-sidebar`: Sidebar layout (mobile stack, desktop sidebar)
- `.dashboard-grid`: Dashboard card grid
- `.form-grid`: Form field grid layout
- `.split-layout`: Two-column split layout

## Component Patterns

### Buttons
```css
.btn-base {
  /* Base button styles */
}

.btn-primary {
  /* Primary button variant */
}

.btn-secondary {
  /* Secondary button variant */
}
```

### Cards
```css
.card-base {
  /* Base card styles with theme-aware colors */
}
```

### Inputs
```css
.input-base {
  /* Base input styles with theme support */
}
```

## Responsive Design

### Breakpoints
- `sm`: 640px (Mobile landscape)
- `md`: 768px (Tablet)
- `lg`: 1024px (Desktop)
- `xl`: 1280px (Large desktop)
- `2xl`: 1536px (Extra large)

### Mobile-First Approach
All utilities are designed mobile-first, with larger screen styles applied progressively.

### Touch Targets
All interactive elements meet the 44px minimum touch target requirement using the `.touch-target` utility.

## Accessibility

### Focus Management
- Custom focus ring using `--color-focus-ring`
- High contrast focus indicators
- Keyboard navigation support

### Color Contrast
- All color combinations meet WCAG 2.1 AA standards
- Minimum 4.5:1 contrast ratio for normal text
- Minimum 3:1 contrast ratio for large text

### Screen Reader Support
- `.sr-only` utility for screen reader only content
- Semantic HTML structure encouraged
- Proper ARIA attributes in components

## Usage Examples

### Basic Layout
```html
<div class="container-responsive section-spacing">
  <div class="stack-lg">
    <h1 class="text-heading-1">Page Title</h1>
    <p class="text-paragraph">Page description</p>
    <div class="card-grid">
      <!-- Cards here -->
    </div>
  </div>
</div>
```

### Form Layout
```html
<form class="form-grid">
  <div class="form-group">
    <label class="text-label">Field Label</label>
    <input class="input-base" type="text" />
    <p class="text-helper">Helper text</p>
  </div>
</form>
```

### Dashboard Layout
```html
<div class="dashboard-main">
  <aside class="sidebar">
    <!-- Navigation -->
  </aside>
  <main class="container-fluid">
    <div class="dashboard-grid">
      <!-- Dashboard cards -->
    </div>
  </main>
</div>
```

## Performance Considerations

- CSS custom properties enable efficient theme switching
- Utility classes reduce CSS bundle size
- Responsive utilities minimize media query duplication
- Critical CSS is inlined for faster initial render

## Browser Support

- Modern browsers with CSS custom properties support
- Graceful degradation for older browsers
- Progressive enhancement approach