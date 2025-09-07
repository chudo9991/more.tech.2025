<template>
  <div class="ai-avatar" :style="{ width: size + 'px', height: size + 'px' }">
    <svg 
      :width="size" 
      :height="size" 
      viewBox="0 0 100 100" 
      xmlns="http://www.w3.org/2000/svg"
      class="ai-avatar-svg"
    >
      <defs>
        <linearGradient id="detroitGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="primaryColor" stop-opacity="0.9"/>
        </linearGradient>
        
        <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Triangles distributed across entire circle area (viewBox 0-100) -->
      <!-- Top area -->
      <polygon points="15,15 25,15 20,25" fill="url(#detroitGradient)" opacity="0.7" class="triangle triangle-1"/>
      <polygon points="40,10 50,10 45,20" fill="url(#detroitGradient)" opacity="0.6" class="triangle triangle-2"/>
      <polygon points="70,15 80,15 75,25" fill="url(#detroitGradient)" opacity="0.8" class="triangle triangle-3"/>
      
      <!-- Left area -->
      <polygon points="10,35 20,35 15,45" fill="url(#detroitGradient)" opacity="0.5" class="triangle triangle-4"/>
      <polygon points="15,55 25,55 20,65" fill="url(#detroitGradient)" opacity="0.9" class="triangle triangle-5"/>
      
      <!-- Right area -->
      <polygon points="75,40 85,40 80,50" fill="url(#detroitGradient)" opacity="0.4" class="triangle triangle-6"/>
      <polygon points="80,65 90,65 85,75" fill="url(#detroitGradient)" opacity="0.6" class="triangle triangle-7"/>
      
      <!-- Bottom area -->
      <polygon points="25,80 35,80 30,90" fill="url(#detroitGradient)" opacity="0.8" class="triangle triangle-8"/>
      <polygon points="50,85 60,85 55,95" fill="url(#detroitGradient)" opacity="0.5" class="triangle triangle-9"/>
      <polygon points="70,80 80,80 75,90" fill="url(#detroitGradient)" opacity="0.7" class="triangle triangle-10"/>
      
      <!-- Center area -->
      <polygon points="35,30 45,30 40,40" fill="url(#detroitGradient)" opacity="0.6" class="triangle triangle-11"/>
      <polygon points="55,35 65,35 60,45" fill="url(#detroitGradient)" opacity="0.4" class="triangle triangle-12"/>
      <polygon points="30,50 40,50 35,60" fill="url(#detroitGradient)" opacity="0.8" class="triangle triangle-13"/>
      <polygon points="60,55 70,55 65,65" fill="url(#detroitGradient)" opacity="0.3" class="triangle triangle-14"/>
      <polygon points="45,45 55,45 50,55" fill="url(#detroitGradient)" opacity="0.5" class="triangle triangle-15"/>
      
      <!-- Additional scattered triangles -->
      <polygon points="25,40 30,40 27.5,45" fill="url(#detroitGradient)" opacity="0.7" class="triangle triangle-16"/>
      <polygon points="65,25 70,25 67.5,30" fill="url(#detroitGradient)" opacity="0.6" class="triangle triangle-17"/>
      <polygon points="40,70 45,70 42.5,75" fill="url(#detroitGradient)" opacity="0.4" class="triangle triangle-18"/>
    </svg>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: number
  primaryColor?: string
  secondaryColor?: string
  accentColor?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 80,
  primaryColor: '#00ffff',
  secondaryColor: '#8a2be2',
  accentColor: '#ff1493'
})
</script>

<style scoped>
.ai-avatar {
  display: inline-block;
  position: relative;
  background: transparent;
}

.ai-avatar-svg {
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.4));
}

.triangle {
  animation: triangleFloat 4s ease-in-out infinite;
}

/* Different speeds and delays for each triangle */
.triangle-1 { animation-duration: 3s; animation-delay: 0s; }
.triangle-2 { animation-duration: 4.5s; animation-delay: 0.2s; }
.triangle-3 { animation-duration: 3.8s; animation-delay: 0.4s; }
.triangle-4 { animation-duration: 5s; animation-delay: 0.6s; }
.triangle-5 { animation-duration: 2.8s; animation-delay: 0.8s; }
.triangle-6 { animation-duration: 4.2s; animation-delay: 1s; }
.triangle-7 { animation-duration: 3.5s; animation-delay: 1.2s; }
.triangle-8 { animation-duration: 4.8s; animation-delay: 1.4s; }
.triangle-9 { animation-duration: 3.2s; animation-delay: 1.6s; }
.triangle-10 { animation-duration: 4.6s; animation-delay: 1.8s; }
.triangle-11 { animation-duration: 2.5s; animation-delay: 2s; }
.triangle-12 { animation-duration: 3.9s; animation-delay: 2.2s; }
.triangle-13 { animation-duration: 4.1s; animation-delay: 2.4s; }
.triangle-14 { animation-duration: 3.7s; animation-delay: 2.6s; }
.triangle-15 { animation-duration: 4.3s; animation-delay: 2.8s; }
.triangle-16 { animation-duration: 3.6s; animation-delay: 3s; }
.triangle-17 { animation-duration: 4s; animation-delay: 3.2s; }
.triangle-18 { animation-duration: 3.3s; animation-delay: 3.4s; }

@keyframes triangleFloat {
  0%, 100% { 
    transform: translate(0px, 0px) rotate(0deg);
    opacity: 0.3;
  }
  25% { 
    transform: translate(4px, -6px) rotate(8deg);
    opacity: 0.8;
  }
  50% { 
    transform: translate(-3px, -8px) rotate(-5deg);
    opacity: 0.6;
  }
  75% { 
    transform: translate(-5px, -3px) rotate(10deg);
    opacity: 0.9;
  }
}

.ai-avatar:hover .ai-avatar-svg {
  filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.7));
}

.ai-avatar:hover .triangle {
  animation-duration: 2s !important;
}

.ai-avatar:hover .triangle {
  opacity: 1 !important;
}
</style>