<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="2" y="7" width="20" height="12" rx="2" :fill="color" opacity="0.8"/>
    <path d="M16 7V5C16 3.9 15.1 3 14 3H10C8.9 3 8 3.9 8 5V7" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="9" y="12" width="6" height="2" rx="1" fill="white"/>
    <circle cx="6" cy="13" r="1" fill="white" opacity="0.6"/>
    <circle cx="18" cy="13" r="1" fill="white" opacity="0.6"/>
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: [String, Number],
    default: 24
  },
  color: {
    type: String,
    default: 'currentColor'
  }
})
</script>