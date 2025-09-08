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
        <linearGradient id="brainGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="30%" stop-color="#8a2be2" stop-opacity="0.8"/>
          <stop offset="70%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
        
        <filter id="brainGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Main brain structure -->
      <path 
        d="M21.33 12.91C21.42 12.62 21.46 12.31 21.46 12C21.46 11.69 21.42 11.38 21.33 11.09C21.42 10.8 21.46 10.49 21.46 10.18C21.46 8.18 19.96 6.5 18 6.5C17.69 6.5 17.38 6.54 17.09 6.63C16.8 6.54 16.49 6.5 16.18 6.5C14.18 6.5 12.5 8 12.5 10C12.5 10.31 12.54 10.62 12.63 10.91C12.54 11.2 12.5 11.51 12.5 11.82C12.5 13.82 14 15.5 16 15.5C16.31 15.5 16.62 15.46 16.91 15.37C17.2 15.46 17.51 15.5 17.82 15.5C19.82 15.5 21.5 14 21.5 12C21.5 11.69 21.46 11.38 21.37 11.09C21.46 11.38 21.5 11.69 21.5 12C21.5 12.31 21.46 12.62 21.37 12.91H21.33Z" 
        fill="url(#brainGradient)" 
        class="brain-right"
      />
      
      <!-- Left hemisphere -->
      <path 
        d="M9 12C9 10.34 7.66 9 6 9C4.34 9 3 10.34 3 12C3 13.66 4.34 15 6 15C7.66 15 9 13.66 9 12Z" 
        fill="url(#brainGradient)" 
        class="brain-left"
      />
      
      <!-- Brain stem -->
      <path 
        d="M15.5 18C15.5 16.34 14.16 15 12.5 15C10.84 15 9.5 16.34 9.5 18C9.5 19.66 10.84 21 12.5 21C14.16 21 15.5 19.66 15.5 18Z" 
        fill="url(#brainGradient)" 
        class="brain-stem"
      />
      
      <!-- Central node -->
      <circle 
        cx="12" 
        cy="8" 
        r="2" 
        fill="url(#brainGradient)" 
        class="brain-center"
      />
      
      <!-- Neural connections (animated lines) -->
      <g class="neural-connections" stroke="url(#brainGradient)" stroke-width="0.5" fill="none" opacity="0.6">
        <path d="M6 12 Q9 10 12 8" class="connection connection-1"/>
        <path d="M12 8 Q15 10 18 12" class="connection connection-2"/>
        <path d="M12 8 Q12 12 12.5 15" class="connection connection-3"/>
        <path d="M6 12 Q9 15 12.5 18" class="connection connection-4"/>
        <path d="M18 12 Q15 15 12.5 18" class="connection connection-5"/>
      </g>
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconBrain',
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
  filter: drop-shadow(0 0 8px rgba(138, 43, 226, 0.4));
  transition: all 0.3s ease;
}

.brain-right {
  animation: brainPulse 3s ease-in-out infinite;
}

.brain-left {
  animation: brainPulse 3s ease-in-out infinite;
  animation-delay: 0.5s;
}

.brain-center {
  animation: centerPulse 2s ease-in-out infinite;
}

.brain-stem {
  animation: stemGlow 4s ease-in-out infinite;
}

.connection {
  stroke-dasharray: 5, 5;
  animation: neuralFlow 2s linear infinite;
}

.connection-1 { animation-delay: 0s; }
.connection-2 { animation-delay: 0.2s; }
.connection-3 { animation-delay: 0.4s; }
.connection-4 { animation-delay: 0.6s; }
.connection-5 { animation-delay: 0.8s; }

@keyframes brainPulse {
  0%, 100% {
    opacity: 0.8;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
}

@keyframes centerPulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@keyframes stemGlow {
  0%, 100% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
}

@keyframes neuralFlow {
  0% {
    stroke-dashoffset: 0;
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    stroke-dashoffset: -10;
    opacity: 0.3;
  }
}

/* Enhanced hover effects */
.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(138, 43, 226, 0.8)) 
          drop-shadow(0 0 25px rgba(0, 255, 255, 0.4))
          drop-shadow(0 0 35px rgba(255, 20, 147, 0.3));
  animation: brainGlow 1.5s ease-in-out infinite;
}

.icon-wrapper:hover .brain-right,
.icon-wrapper:hover .brain-left {
  animation-duration: 1.5s;
}

.icon-wrapper:hover .brain-center {
  animation-duration: 1s;
}

.icon-wrapper:hover .connection {
  animation-duration: 1s;
  opacity: 1 !important;
  stroke-width: 1;
}

@keyframes brainGlow {
  0%, 100% {
    filter: drop-shadow(0 0 15px rgba(138, 43, 226, 0.8)) 
            drop-shadow(0 0 25px rgba(0, 255, 255, 0.4))
            drop-shadow(0 0 35px rgba(255, 20, 147, 0.3));
  }
  50% {
    filter: drop-shadow(0 0 25px rgba(138, 43, 226, 1)) 
            drop-shadow(0 0 35px rgba(0, 255, 255, 0.6))
            drop-shadow(0 0 45px rgba(255, 20, 147, 0.5));
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .brain-right,
  .brain-left,
  .brain-center,
  .brain-stem,
  .connection {
    animation: none;
  }
  
  .icon-wrapper:hover .icon-svg {
    animation: none;
  }
}
</style>