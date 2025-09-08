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
        <linearGradient id="briefcaseGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Briefcase body -->
      <rect 
        x="3" 
        y="8" 
        width="18" 
        height="12" 
        rx="2" 
        fill="url(#briefcaseGradient)" 
        class="briefcase-body"
      />
      
      <!-- Briefcase handle -->
      <path 
        d="M8 8V6C8 4.9 8.9 4 10 4H14C15.1 4 16 4.9 16 6V8" 
        stroke="url(#briefcaseGradient)" 
        stroke-width="2" 
        fill="none"
        stroke-linecap="round"
        class="briefcase-handle"
      />
      
      <!-- Briefcase lock -->
      <rect 
        x="11" 
        y="12" 
        width="2" 
        height="4" 
        rx="1" 
        fill="url(#briefcaseGradient)" 
        class="briefcase-lock"
      />
      
      <!-- Briefcase clasps -->
      <circle cx="6" cy="14" r="1" fill="url(#briefcaseGradient)" class="clasp clasp-1"/>
      <circle cx="18" cy="14" r="1" fill="url(#briefcaseGradient)" class="clasp clasp-2"/>
      
      <!-- Briefcase divider -->
      <line 
        x1="3" 
        y1="14" 
        x2="21" 
        y2="14" 
        stroke="url(#briefcaseGradient)" 
        stroke-width="1" 
        opacity="0.5"
        class="divider"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconBriefcase',
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
  filter: drop-shadow(0 0 8px rgba(153, 50, 204, 0.4));
  transition: all 0.3s ease;
}

.briefcase-body {
  animation: briefcaseFloat 2.5s ease-in-out infinite;
}

.briefcase-handle {
  animation: handleShine 3s ease-in-out infinite;
}

.briefcase-lock {
  animation: lockGlow 2s ease-in-out infinite;
}

.clasp {
  animation: claspPulse 1.8s ease-in-out infinite;
}

.clasp-1 { animation-delay: 0s; }
.clasp-2 { animation-delay: 0.9s; }

.divider {
  animation: dividerShimmer 2.5s ease-in-out infinite;
}

@keyframes briefcaseFloat {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.9;
  }
  50% {
    transform: translateY(-1px);
    opacity: 1;
  }
}

@keyframes handleShine {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes lockGlow {
  0%, 100% {
    opacity: 0.7;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

@keyframes claspPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes dividerShimmer {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.7;
  }
}

/* Enhanced hover effects */
.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(153, 50, 204, 0.8)) 
          drop-shadow(0 0 25px rgba(0, 255, 255, 0.4));
  animation: briefcaseGlow 1s ease-in-out infinite;
}

.icon-wrapper:hover .briefcase-body {
  animation-duration: 1.5s;
}

.icon-wrapper:hover .briefcase-lock {
  animation-duration: 1s;
}

.icon-wrapper:hover .clasp {
  animation-duration: 1s;
}

@keyframes briefcaseGlow {
  0%, 100% {
    filter: drop-shadow(0 0 15px rgba(153, 50, 204, 0.8)) 
            drop-shadow(0 0 25px rgba(0, 255, 255, 0.4));
  }
  50% {
    filter: drop-shadow(0 0 20px rgba(153, 50, 204, 1)) 
            drop-shadow(0 0 35px rgba(0, 255, 255, 0.6));
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .briefcase-body,
  .briefcase-handle,
  .briefcase-lock,
  .clasp,
  .divider {
    animation: none;
  }
  
  .icon-wrapper:hover .icon-svg {
    animation: none;
  }
}
</style>