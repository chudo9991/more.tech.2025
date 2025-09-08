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
        <linearGradient id="chartGradient" x1="0%" y1="100%" x2="0%" y2="0%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#4fc3f7" stop-opacity="0.7"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.9"/>
        </linearGradient>
        
        <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.8"/>
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0.8"/>
        </linearGradient>
        
        <filter id="chartGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Axes -->
      <path 
        d="M3 3V21H21" 
        stroke="url(#lineGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="chart-axes"
      />
      
      <!-- Trend line -->
      <path 
        d="M9 9L12 6L16 10L20 6" 
        stroke="url(#lineGradient)" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="trend-line"
      />
      
      <!-- Data bars -->
      <rect 
        x="7" 
        y="12" 
        width="2" 
        height="8" 
        fill="url(#chartGradient)" 
        class="bar bar-1"
      />
      <rect 
        x="11" 
        y="8" 
        width="2" 
        height="12" 
        fill="url(#chartGradient)" 
        class="bar bar-2"
      />
      <rect 
        x="15" 
        y="14" 
        width="2" 
        height="6" 
        fill="url(#chartGradient)" 
        class="bar bar-3"
      />
      <rect 
        x="19" 
        y="10" 
        width="2" 
        height="10" 
        fill="url(#chartGradient)" 
        class="bar bar-4"
      />
      
      <!-- Data points on trend line -->
      <circle cx="9" cy="9" r="1.5" fill="url(#chartGradient)" class="data-point point-1"/>
      <circle cx="12" cy="6" r="1.5" fill="url(#chartGradient)" class="data-point point-2"/>
      <circle cx="16" cy="10" r="1.5" fill="url(#chartGradient)" class="data-point point-3"/>
      <circle cx="20" cy="6" r="1.5" fill="url(#chartGradient)" class="data-point point-4"/>
    </svg>
  </div>
</template>

<script>
export default {
  name: 'IconChart',
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

.chart-axes {
  animation: axesGlow 3s ease-in-out infinite;
}

.trend-line {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  animation: lineGrow 2s ease-out infinite;
}

.bar {
  animation: barGrow 2s ease-out infinite;
  transform-origin: bottom;
}

.bar-1 { animation-delay: 0.2s; }
.bar-2 { animation-delay: 0.4s; }
.bar-3 { animation-delay: 0.6s; }
.bar-4 { animation-delay: 0.8s; }

.data-point {
  animation: pointPulse 1.5s ease-in-out infinite;
}

.point-1 { animation-delay: 0.2s; }
.point-2 { animation-delay: 0.4s; }
.point-3 { animation-delay: 0.6s; }
.point-4 { animation-delay: 0.8s; }

@keyframes axesGlow {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes lineGrow {
  0% {
    stroke-dashoffset: 20;
    opacity: 0.5;
  }
  100% {
    stroke-dashoffset: 0;
    opacity: 1;
  }
}

@keyframes barGrow {
  0% {
    transform: scaleY(0);
    opacity: 0.5;
  }
  100% {
    transform: scaleY(1);
    opacity: 1;
  }
}

@keyframes pointPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.3);
    opacity: 1;
  }
}

/* Enhanced hover effects */
.icon-wrapper:hover .icon-svg {
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
          drop-shadow(0 0 25px rgba(255, 20, 147, 0.4))
          drop-shadow(0 0 35px rgba(76, 195, 247, 0.3));
  animation: chartGlow 1s ease-in-out infinite;
}

.icon-wrapper:hover .trend-line {
  animation-duration: 1s;
  stroke-width: 3;
}

.icon-wrapper:hover .bar {
  animation-duration: 1s;
}

.icon-wrapper:hover .data-point {
  animation-duration: 0.8s;
}

.icon-wrapper:hover .chart-axes {
  stroke-width: 3;
}

@keyframes chartGlow {
  0%, 100% {
    filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.8)) 
            drop-shadow(0 0 25px rgba(255, 20, 147, 0.4))
            drop-shadow(0 0 35px rgba(76, 195, 247, 0.3));
  }
  50% {
    filter: drop-shadow(0 0 25px rgba(0, 255, 255, 1)) 
            drop-shadow(0 0 35px rgba(255, 20, 147, 0.6))
            drop-shadow(0 0 45px rgba(76, 195, 247, 0.5));
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .chart-axes,
  .trend-line,
  .bar,
  .data-point {
    animation: none;
  }
  
  .icon-wrapper:hover .icon-svg {
    animation: none;
  }
}
</style>