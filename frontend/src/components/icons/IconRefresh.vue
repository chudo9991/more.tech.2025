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
        <linearGradient id="refreshGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Refresh arrow -->
      <path 
        d="M23 4V10H17" 
        stroke="url(#refreshGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="refresh-arrow-1"
      />
      
      <!-- Refresh circle -->
      <path 
        d="M20.49 15C19.9 17.5 17.76 19.5 15 19.5C11.5 19.5 8.5 16.5 8.5 13S11.5 6.5 15 6.5C16.61 6.5 18.09 7.28 19.05 8.57L23 4" 
        stroke="url(#refreshGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="refresh-circle"
      />
      
      <!-- Second arrow -->
      <path 
        d="M1 20V14H7" 
        stroke="url(#refreshGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="refresh-arrow-2"
      />
      
      <!-- Second circle -->
      <path 
        d="M3.51 9C4.1 6.5 6.24 4.5 9 4.5C12.5 4.5 15.5 7.5 15.5 11S12.5 17.5 9 17.5C7.39 17.5 5.91 16.72 4.95 15.43L1 20" 
        stroke="url(#refreshGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="refresh-circle-2"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconRefresh',
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

.refresh-arrow-1,
.refresh-circle {
  animation: refreshSpin 2s ease-in-out infinite;
  transform-origin: 12px 12px;
}

.refresh-arrow-2,
.refresh-circle-2 {
  animation: refreshSpin 2s ease-in-out infinite reverse;
  transform-origin: 12px 12px;
  animation-delay: 1s;
}

@keyframes refreshSpin {
  0% {
    transform: rotate(0deg);
    opacity: 0.8;
  }
  50% {
    transform: rotate(180deg);
    opacity: 1;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.8;
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.8));
}

.icon-wrapper:hover .refresh-arrow-1,
.icon-wrapper:hover .refresh-circle,
.icon-wrapper:hover .refresh-arrow-2,
.icon-wrapper:hover .refresh-circle-2 {
  animation-duration: 1s;
}

@media (prefers-reduced-motion: reduce) {
  .refresh-arrow-1,
  .refresh-circle,
  .refresh-arrow-2,
  .refresh-circle-2 {
    animation: none;
  }
}
</style>