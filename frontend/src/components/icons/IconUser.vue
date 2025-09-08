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
        <linearGradient id="userGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- User head -->
      <circle 
        cx="12" 
        cy="8" 
        r="4" 
        fill="url(#userGradient)" 
        class="user-head"
      />
      
      <!-- User body -->
      <path 
        d="M20 21V19C20 16.79 16.42 15 12 15S4 16.79 4 19V21" 
        stroke="url(#userGradient)" 
        stroke-width="2" 
        fill="none"
        stroke-linecap="round"
        class="user-body"
      />
      
      <!-- Highlight on head -->
      <circle 
        cx="10" 
        cy="6" 
        r="1" 
        fill="rgba(255, 255, 255, 0.6)" 
        class="head-highlight"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconUser',
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

.user-head {
  animation: headFloat 2.5s ease-in-out infinite;
}

.user-body {
  animation: bodyGlow 3s ease-in-out infinite;
}

.head-highlight {
  animation: highlightPulse 2s ease-in-out infinite;
}

@keyframes headFloat {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.9;
  }
  50% {
    transform: translateY(-1px);
    opacity: 1;
  }
}

@keyframes bodyGlow {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes highlightPulse {
  0%, 100% {
    opacity: 0.4;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.2);
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
          drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
}

.icon-wrapper:hover .user-head {
  animation-duration: 1.5s;
}

.icon-wrapper:hover .user-body {
  stroke-width: 3;
}

@media (prefers-reduced-motion: reduce) {
  .user-head,
  .user-body,
  .head-highlight {
    animation: none;
  }
}
</style>