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
        <linearGradient id="deleteGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ef4444" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#f87171" stop-opacity="0.7"/>
          <stop offset="100%" stop-color="#dc2626" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Trash can body -->
      <path 
        d="M3 6H5H21" 
        stroke="url(#deleteGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="trash-top"
      />
      
      <!-- Trash can -->
      <path 
        d="M19 6V20C19 21 18 22 17 22H7C6 22 5 21 5 20V6M8 6V4C8 3 9 2 10 2H14C15 2 16 3 16 4V6" 
        stroke="url(#deleteGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="trash-body"
      />
      
      <!-- Trash lines -->
      <line 
        x1="10" 
        y1="11" 
        x2="10" 
        y2="17" 
        stroke="url(#deleteGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="trash-line line-1"
      />
      <line 
        x1="14" 
        y1="11" 
        x2="14" 
        y2="17" 
        stroke="url(#deleteGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="trash-line line-2"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconDelete',
  props: {
    size: {
      type: [String, Number],
      default: 16
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
  filter: drop-shadow(0 0 4px rgba(239, 68, 68, 0.4));
  transition: all 0.3s ease;
}

.trash-top {
  animation: topShake 2s ease-in-out infinite;
}

.trash-body {
  animation: bodyFloat 2.5s ease-in-out infinite;
}

.trash-line {
  animation: lineGlow 1.8s ease-in-out infinite;
}

.line-1 { animation-delay: 0s; }
.line-2 { animation-delay: 0.9s; }

@keyframes topShake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-0.5px);
  }
  75% {
    transform: translateX(0.5px);
  }
}

@keyframes bodyFloat {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.9;
  }
  50% {
    transform: translateY(-1px);
    opacity: 1;
  }
}

@keyframes lineGlow {
  0%, 100% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.8));
}

.icon-wrapper:hover .trash-top {
  animation-duration: 1s;
}

@media (prefers-reduced-motion: reduce) {
  .trash-top,
  .trash-body,
  .trash-line {
    animation: none;
  }
}
</style>