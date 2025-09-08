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
        <linearGradient id="starGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#ffd700" stop-opacity="0.8"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Star shape -->
      <path 
        d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" 
        fill="url(#starGradient)" 
        class="star-body"
      />
      
      <!-- Star highlights -->
      <path 
        d="M12 2L13.5 6.5L12 8L10.5 6.5L12 2Z" 
        fill="rgba(255, 255, 255, 0.4)" 
        class="star-highlight-1"
      />
      <path 
        d="M17 14L19 16L17 18L15 16L17 14Z" 
        fill="rgba(255, 255, 255, 0.3)" 
        class="star-highlight-2"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconStar',
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
  filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4));
  transition: all 0.3s ease;
}

.star-body {
  animation: starTwinkle 2.5s ease-in-out infinite;
}

.star-highlight-1 {
  animation: highlightShimmer 2s ease-in-out infinite;
}

.star-highlight-2 {
  animation: highlightShimmer 2s ease-in-out infinite;
  animation-delay: 1s;
}

@keyframes starTwinkle {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.05) rotate(5deg);
    opacity: 1;
  }
}

@keyframes highlightShimmer {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.6;
  }
}

.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.8)) 
          drop-shadow(0 0 25px rgba(0, 255, 255, 0.4))
          drop-shadow(0 0 35px rgba(255, 20, 147, 0.3));
}

.icon-wrapper:hover .star-body {
  animation-duration: 1.5s;
}

.icon-wrapper:hover .star-highlight-1,
.icon-wrapper:hover .star-highlight-2 {
  animation-duration: 1s;
}

@media (prefers-reduced-motion: reduce) {
  .star-body,
  .star-highlight-1,
  .star-highlight-2 {
    animation: none;
  }
}
</style>