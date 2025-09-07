<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4" y="8" width="16" height="12" rx="2" :fill="color" opacity="0.8"/>
    <circle cx="8.5" cy="12" r="1.5" fill="white"/>
    <circle cx="15.5" cy="12" r="1.5" fill="white"/>
    <rect x="10" y="15" width="4" height="1" rx="0.5" fill="white"/>
    <rect x="11" y="4" width="2" height="4" :fill="color"/>
    <circle cx="12" cy="4" r="1" :fill="color"/>
    <rect x="2" y="10" width="2" height="4" rx="1" :fill="color"/>
    <rect x="20" y="10" width="2" height="4" rx="1" :fill="color"/>
    <rect x="6" y="20" width="2" height="2" rx="1" :fill="color"/>
    <rect x="16" y="20" width="2" height="2" rx="1" :fill="color"/>
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