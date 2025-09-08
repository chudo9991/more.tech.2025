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
        <linearGradient id="viewGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Eye shape -->
      <path 
        d="M1 12S5 4 12 4S23 12 23 12S19 20 12 20S1 12 1 12Z" 
        stroke="url(#viewGradient)" 
        stroke-width="2" 
        fill="none"
        class="eye-shape"
      />
      
      <!-- Pupil -->
      <circle 
        cx="12" 
        cy="12" 
        r="3" 
        fill="url(#viewGradient)" 
        class="pupil"
      />
      
      <!-- Highlight -->
      <circle 
        cx="13" 
        cy="11" 
        r="1" 
        fill="rgba(255, 255, 255, 0.6)" 
        class="highlight"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconView',
  props: {
    size: {
      type: [String, Number],
      default: 16
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
  filter: drop-shadow(0 0 4px rgba(0, 255, 255, 0.4));
  transition: all 0.3s ease;
}

.eye-shape {
  animation: eyeBlink 3s ease-in-out infinite;
}

.pupil {
  animation: pupilMove 2s ease-in-out infinite;
}

.highlight {
  animation: highlightShine 2s ease-in-out infinite;
}

@keyframes eyeBlink {
  0%, 90%, 100% {
    opacity: 1;
  }
  95% {
    opacity: 0.3;
  }
}

@keyframes pupilMove {
  0%, 100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(1px, -1px);
  }
}

@keyframes highlightShine {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.8;
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.8));
}

@media (prefers-reduced-motion: reduce) {
  .eye-shape,
  .pupil,
  .highlight {
    animation: none;
  }
}
</style>