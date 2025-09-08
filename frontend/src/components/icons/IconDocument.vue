<template>
  <div class="icon-wrapper" :style="{ width: size + 'px', height: size + 'px' }">
    <svg 
      :width="size" 
      :height="size" 
      viewBox="0 0 24 24" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      class="icon-svg"
    >
      <defs>
        <linearGradient id="docGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Document body -->
      <path 
        d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2Z" 
        fill="url(#docGradient)" 
        class="doc-body"
      />
      
      <!-- Document corner fold -->
      <path 
        d="M14 2V8H20" 
        fill="none" 
        stroke="url(#docGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="doc-fold"
      />
      
      <!-- Document lines -->
      <line 
        x1="7" 
        y1="10" 
        x2="17" 
        y2="10" 
        stroke="url(#docGradient)" 
        stroke-width="1.5" 
        stroke-linecap="round"
        class="doc-line line-1"
      />
      <line 
        x1="7" 
        y1="13" 
        x2="17" 
        y2="13" 
        stroke="url(#docGradient)" 
        stroke-width="1.5" 
        stroke-linecap="round"
        class="doc-line line-2"
      />
      <line 
        x1="7" 
        y1="16" 
        x2="14" 
        y2="16" 
        stroke="url(#docGradient)" 
        stroke-width="1.5" 
        stroke-linecap="round"
        class="doc-line line-3"
      />
      
      <!-- Highlight effect -->
      <rect 
        x="6.5" 
        y="9.5" 
        width="11" 
        height="1" 
        fill="url(#docGradient)" 
        opacity="0.3"
        class="highlight"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconDocument',
  props: {
    size: {
      type: [String, Number],
      default: 24
    },
    primaryColor: {
      type: String,
      default: '#00ffff'
    },
    accentColor: {
      type: String,
      default: '#ff1493'
    }
  }
}
</script>

<style scoped>
.icon-wrapper {
  display: inline-block;
  position: relative;
}

.icon-svg {
  filter: drop-shadow(0 0 8px rgba(255, 20, 147, 0.4));
  transition: all 0.3s ease;
}

.doc-body {
  animation: docFloat 3s ease-in-out infinite;
}

.doc-fold {
  animation: foldShimmer 2s ease-in-out infinite;
}

.doc-line {
  stroke-dasharray: 10, 2;
  animation: lineWrite 2s ease-in-out infinite;
}

.line-1 { animation-delay: 0.2s; }
.line-2 { animation-delay: 0.4s; }
.line-3 { animation-delay: 0.6s; }

.highlight {
  animation: highlightSweep 3s ease-in-out infinite;
}

@keyframes docFloat {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.9;
  }
  50% {
    transform: translateY(-2px);
    opacity: 1;
  }
}

@keyframes foldShimmer {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

@keyframes lineWrite {
  0% {
    stroke-dashoffset: 12;
    opacity: 0.5;
  }
  100% {
    stroke-dashoffset: 0;
    opacity: 1;
  }
}

@keyframes highlightSweep {
  0%, 100% {
    opacity: 0.1;
    transform: scaleX(0);
  }
  50% {
    opacity: 0.5;
    transform: scaleX(1);
  }
}

/* Enhanced hover effects */
.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(255, 20, 147, 0.8)) 
          drop-shadow(0 0 25px rgba(0, 255, 255, 0.4));
  animation: docGlow 1s ease-in-out infinite;
}

.icon-wrapper:hover .doc-body {
  animation-duration: 1.5s;
}

.icon-wrapper:hover .doc-line {
  animation-duration: 1s;
  stroke-width: 2;
}

.icon-wrapper:hover .highlight {
  animation-duration: 1.5s;
  opacity: 0.6 !important;
}

@keyframes docGlow {
  0%, 100% {
    filter: drop-shadow(0 0 15px rgba(255, 20, 147, 0.8)) 
            drop-shadow(0 0 25px rgba(0, 255, 255, 0.4));
  }
  50% {
    filter: drop-shadow(0 0 20px rgba(255, 20, 147, 1)) 
            drop-shadow(0 0 35px rgba(0, 255, 255, 0.6));
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .doc-body,
  .doc-fold,
  .doc-line,
  .highlight {
    animation: none;
  }
  
  .icon-wrapper:hover .icon-svg {
    animation: none;
  }
}
</style>