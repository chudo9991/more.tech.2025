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
        <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Progress circle background -->
      <circle 
        cx="12" 
        cy="12" 
        r="9" 
        stroke="rgba(255, 255, 255, 0.2)" 
        stroke-width="2" 
        fill="none"
        class="progress-bg"
      />
      
      <!-- Progress circle -->
      <circle 
        cx="12" 
        cy="12" 
        r="9" 
        stroke="url(#progressGradient)" 
        stroke-width="2" 
        fill="none"
        stroke-linecap="round"
        stroke-dasharray="56.5"
        stroke-dashoffset="14"
        class="progress-circle"
      />
      
      <!-- Center play icon -->
      <path 
        d="M10 8L16 12L10 16V8Z" 
        fill="url(#progressGradient)" 
        class="play-icon"
      />
      
      <!-- Progress dots -->
      <circle cx="12" cy="3" r="1" fill="url(#progressGradient)" class="progress-dot dot-1"/>
      <circle cx="21" cy="12" r="1" fill="url(#progressGradient)" class="progress-dot dot-2"/>
      <circle cx="12" cy="21" r="1" fill="url(#progressGradient)" class="progress-dot dot-3"/>
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconProgress',
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

.progress-bg {
  animation: bgPulse 3s ease-in-out infinite;
}

.progress-circle {
  animation: progressFill 3s ease-in-out infinite;
  transform-origin: 12px 12px;
  transform: rotate(-90deg);
}

.play-icon {
  animation: playPulse 2s ease-in-out infinite;
}

.progress-dot {
  animation: dotGlow 2s ease-in-out infinite;
}

.dot-1 { animation-delay: 0s; }
.dot-2 { animation-delay: 0.7s; }
.dot-3 { animation-delay: 1.4s; }

@keyframes bgPulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes progressFill {
  0% {
    stroke-dashoffset: 56.5;
  }
  50% {
    stroke-dashoffset: 14;
  }
  100% {
    stroke-dashoffset: 56.5;
  }
}

@keyframes playPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

@keyframes dotGlow {
  0%, 100% {
    opacity: 0.4;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.3);
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
          drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
}

.icon-wrapper:hover .progress-circle {
  animation-duration: 2s;
  stroke-width: 3;
}

.icon-wrapper:hover .play-icon {
  animation-duration: 1s;
}

@media (prefers-reduced-motion: reduce) {
  .progress-bg,
  .progress-circle,
  .play-icon,
  .progress-dot {
    animation: none;
  }
}
</style>