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
        <linearGradient id="robotGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
      </defs>
      
      <!-- Robot head -->
      <rect 
        x="6" 
        y="4" 
        width="12" 
        height="10" 
        rx="2" 
        fill="url(#robotGradient)" 
        class="robot-head"
      />
      
      <!-- Robot eyes -->
      <circle cx="9" cy="8" r="1.5" fill="url(#robotGradient)" class="robot-eye eye-1"/>
      <circle cx="15" cy="8" r="1.5" fill="url(#robotGradient)" class="robot-eye eye-2"/>
      
      <!-- Robot mouth -->
      <rect 
        x="10" 
        y="11" 
        width="4" 
        height="1" 
        rx="0.5" 
        fill="url(#robotGradient)" 
        class="robot-mouth"
      />
      
      <!-- Robot body -->
      <rect 
        x="8" 
        y="14" 
        width="8" 
        height="6" 
        rx="1" 
        fill="url(#robotGradient)" 
        class="robot-body"
      />
      
      <!-- Robot arms -->
      <rect 
        x="4" 
        y="15" 
        width="3" 
        height="4" 
        rx="1" 
        fill="url(#robotGradient)" 
        class="robot-arm arm-left"
      />
      <rect 
        x="17" 
        y="15" 
        width="3" 
        height="4" 
        rx="1" 
        fill="url(#robotGradient)" 
        class="robot-arm arm-right"
      />
      
      <!-- Antenna -->
      <line 
        x1="12" 
        y1="4" 
        x2="12" 
        y2="2" 
        stroke="url(#robotGradient)" 
        stroke-width="2" 
        stroke-linecap="round"
        class="antenna"
      />
      <circle cx="12" cy="2" r="1" fill="url(#robotGradient)" class="antenna-tip"/>
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconRobot',
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

.robot-head {
  animation: headBob 2s ease-in-out infinite;
}

.robot-eye {
  animation: eyeBlink 3s ease-in-out infinite;
}

.eye-1 { animation-delay: 0s; }
.eye-2 { animation-delay: 0.1s; }

.robot-mouth {
  animation: mouthTalk 1.5s ease-in-out infinite;
}

.robot-body {
  animation: bodyPulse 2.5s ease-in-out infinite;
}

.robot-arm {
  animation: armWave 2s ease-in-out infinite;
}

.arm-left { animation-delay: 0s; }
.arm-right { animation-delay: 1s; }

.antenna {
  animation: antennaWiggle 1.8s ease-in-out infinite;
}

.antenna-tip {
  animation: tipGlow 1s ease-in-out infinite;
}

@keyframes headBob {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

@keyframes eyeBlink {
  0%, 90%, 100% {
    transform: scaleY(1);
  }
  95% {
    transform: scaleY(0.1);
  }
}

@keyframes mouthTalk {
  0%, 100% {
    transform: scaleX(1);
  }
  50% {
    transform: scaleX(1.2);
  }
}

@keyframes bodyPulse {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes armWave {
  0%, 100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(10deg);
  }
}

@keyframes antennaWiggle {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(5deg);
  }
  75% {
    transform: rotate(-5deg);
  }
}

@keyframes tipGlow {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.3);
  }
}

/* Enhanced hover effects */
.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
          drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
  animation: robotGlow 1s ease-in-out infinite;
}

.icon-wrapper:hover .robot-head {
  animation-duration: 1s;
}

.icon-wrapper:hover .robot-eye {
  animation-duration: 1.5s;
}

.icon-wrapper:hover .robot-arm {
  animation-duration: 1s;
}

@keyframes robotGlow {
  0%, 100% {
    filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
            drop-shadow(0 0 25px rgba(255, 20, 147, 0.4));
  }
  50% {
    filter: drop-shadow(0 0 20px rgba(0, 255, 255, 1)) 
            drop-shadow(0 0 35px rgba(255, 20, 147, 0.6));
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .robot-head,
  .robot-eye,
  .robot-mouth,
  .robot-body,
  .robot-arm,
  .antenna,
  .antenna-tip {
    animation: none;
  }
  
  .icon-wrapper:hover .icon-svg {
    animation: none;
  }
}
</style>