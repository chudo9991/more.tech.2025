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
        <linearGradient id="micGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
        
        <filter id="micGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Microphone body -->
      <path 
        d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" 
        fill="url(#micGradient)" 
        class="mic-body"
      />
      
      <!-- Sound waves -->
      <path 
        d="M19 10V12C19 16.42 15.42 20 11 20H13C17.42 20 21 16.42 21 12V10H19Z" 
        fill="url(#micGradient)" 
        class="sound-wave wave-1"
        opacity="0.6"
      />
      <path 
        d="M7 12V10H5V12C5 16.42 8.58 20 13 20H11C6.58 20 3 16.42 3 12V10H5V12H7Z" 
        fill="url(#micGradient)" 
        class="sound-wave wave-2"
        opacity="0.6"
      />
      
      <!-- Stand -->
      <path 
        d="M11 22H13V24H11V22Z" 
        fill="url(#micGradient)" 
        class="mic-stand"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconMicrophone',
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
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.4));
  transition: all 0.3s ease;
}

.mic-body {
  animation: micPulse 2s ease-in-out infinite;
}

.sound-wave {
  animation: waveRipple 1.5s ease-in-out infinite;
}

.wave-1 {
  animation-delay: 0.2s;
}

.wave-2 {
  animation-delay: 0.4s;
}

.mic-stand {
  animation: standSway 3s ease-in-out infinite;
}

@keyframes micPulse {
  0%, 100% {
    opacity: 0.8;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
}

@keyframes waveRipple {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
  }
}

@keyframes standSway {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(1deg);
  }
  75% {
    transform: rotate(-1deg);
  }
}

/* Enhanced hover effects */
.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
          drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
  animation: iconGlow 1s ease-in-out infinite;
}

.icon-wrapper:hover .mic-body {
  animation-duration: 1s;
}

.icon-wrapper:hover .sound-wave {
  animation-duration: 0.8s;
  opacity: 1 !important;
}

@keyframes iconGlow {
  0%, 100% {
    filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
            drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
  }
  50% {
    filter: drop-shadow(0 0 20px rgba(0, 255, 255, 1)) 
            drop-shadow(0 0 35px rgba(255, 20, 147, 0.6));
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .mic-body,
  .sound-wave,
  .mic-stand {
    animation: none;
  }
  
  .icon-wrapper:hover .icon-svg {
    animation: none;
  }
}
</style>