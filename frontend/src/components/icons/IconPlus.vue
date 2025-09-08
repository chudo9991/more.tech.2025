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
        <linearGradient id="plusGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Plus horizontal line -->
      <line 
        x1="12" 
        y1="5" 
        x2="12" 
        y2="19" 
        stroke="url(#plusGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="plus-vertical"
      />
      
      <!-- Plus vertical line -->
      <line 
        x1="5" 
        y1="12" 
        x2="19" 
        y2="12" 
        stroke="url(#plusGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="plus-horizontal"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconPlus',
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

.plus-vertical {
  animation: verticalGlow 2s ease-in-out infinite;
}

.plus-horizontal {
  animation: horizontalGlow 2s ease-in-out infinite;
  animation-delay: 1s;
}

@keyframes verticalGlow {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes horizontalGlow {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.8));
}

.icon-wrapper:hover .plus-vertical,
.icon-wrapper:hover .plus-horizontal {
  stroke-width: 3;
  animation-duration: 1s;
}

@media (prefers-reduced-motion: reduce) {
  .plus-vertical,
  .plus-horizontal {
    animation: none;
  }
}
</style>