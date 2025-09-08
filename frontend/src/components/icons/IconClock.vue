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
        <linearGradient id="clockGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Clock face -->
      <circle 
        cx="12" 
        cy="12" 
        r="9" 
        stroke="url(#clockGradient)" 
        stroke-width="2" 
        fill="none"
        class="clock-face"
      />
      
      <!-- Hour markers -->
      <circle cx="12" cy="4" r="1" fill="url(#clockGradient)" class="marker marker-12"/>
      <circle cx="20" cy="12" r="1" fill="url(#clockGradient)" class="marker marker-3"/>
      <circle cx="12" cy="20" r="1" fill="url(#clockGradient)" class="marker marker-6"/>
      <circle cx="4" cy="12" r="1" fill="url(#clockGradient)" class="marker marker-9"/>
      
      <!-- Clock hands -->
      <line 
        x1="12" 
        y1="12" 
        x2="12" 
        y2="8" 
        stroke="url(#clockGradient)" 
        stroke-width="3" 
        stroke-linecap="round"
        class="hour-hand"
      />
      <line 
        x1="12" 
        y1="12" 
        x2="16" 
        y2="12" 
        stroke="url(#clockGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="minute-hand"
      />
      
      <!-- Center dot -->
      <circle 
        cx="12" 
        cy="12" 
        r="2" 
        fill="url(#clockGradient)" 
        class="center-dot"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconClock',
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

.clock-face {
  animation: clockPulse 3s ease-in-out infinite;
}

.marker {
  animation: markerGlow 2s ease-in-out infinite;
}

.marker-12 { animation-delay: 0s; }
.marker-3 { animation-delay: 0.5s; }
.marker-6 { animation-delay: 1s; }
.marker-9 { animation-delay: 1.5s; }

.hour-hand {
  animation: handTick 4s ease-in-out infinite;
  transform-origin: 12px 12px;
}

.minute-hand {
  animation: handTick 2s ease-in-out infinite;
  transform-origin: 12px 12px;
}

.center-dot {
  animation: centerPulse 1.5s ease-in-out infinite;
}

@keyframes clockPulse {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes markerGlow {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@keyframes handTick {
  0%, 100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(6deg);
  }
}

@keyframes centerPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
          drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
}

.icon-wrapper:hover .hour-hand,
.icon-wrapper:hover .minute-hand {
  animation-duration: 1s;
  stroke-width: 4;
}

@media (prefers-reduced-motion: reduce) {
  .clock-face,
  .marker,
  .hour-hand,
  .minute-hand,
  .center-dot {
    animation: none;
  }
}
</style>