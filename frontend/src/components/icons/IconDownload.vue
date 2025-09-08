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
        <linearGradient id="downloadGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Download arrow -->
      <path 
        d="M21 15V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V15" 
        stroke="url(#downloadGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="download-base"
      />
      
      <!-- Arrow shaft -->
      <line 
        x1="12" 
        y1="3" 
        x2="12" 
        y2="15" 
        stroke="url(#downloadGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="arrow-shaft"
      />
      
      <!-- Arrow head -->
      <path 
        d="M7 10L12 15L17 10" 
        stroke="url(#downloadGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="arrow-head"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconDownload',
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

.download-base {
  animation: baseGlow 2s ease-in-out infinite;
}

.arrow-shaft {
  animation: shaftMove 1.5s ease-in-out infinite;
}

.arrow-head {
  animation: headBounce 1.5s ease-in-out infinite;
}

@keyframes baseGlow {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes shaftMove {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(2px);
  }
}

@keyframes headBounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(2px);
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.8));
}

.icon-wrapper:hover .arrow-shaft,
.icon-wrapper:hover .arrow-head {
  animation-duration: 0.8s;
}

@media (prefers-reduced-motion: reduce) {
  .download-base,
  .arrow-shaft,
  .arrow-head {
    animation: none;
  }
}
</style>