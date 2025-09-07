<template>
  <component
    v-if="iconComponent && !hasError"
    :is="iconComponent"
    :class="iconClasses"
    @error="handleError"
  />
  <div
    v-else-if="fallbackIcon && !hasError"
    :class="iconClasses"
    v-html="fallbackIcon"
  />
  <div
    v-else
    :class="[iconClasses, 'fallback-icon']"
    :title="name"
  >
    <svg
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fill-rule="evenodd"
        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
        clip-rule="evenodd"
      />
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

// Heroicons imports
import {
  HomeIcon,
  BriefcaseIcon,
  DocumentIcon,
  UsersIcon,
  ChatBubbleLeftRightIcon,
  CpuChipIcon,
  CogIcon,
  ChartBarIcon,
  FolderIcon,
  ClipboardDocumentListIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  UserIcon,
  ChevronDownIcon,
  ChevronLeftIcon,
  ArrowRightOnRectangleIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  PlayIcon,
  PauseIcon,
  DocumentDuplicateIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  InformationCircleIcon,
  ClockIcon,
  BoltIcon
} from '@heroicons/vue/24/outline'

export interface BaseIconProps {
  name: string
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'outline' | 'solid'
  color?: string
  fallback?: string
}

const props = withDefaults(defineProps<BaseIconProps>(), {
  size: 'md',
  variant: 'outline'
})

// Error handling
const hasError = ref(false)

// Icon registry
const iconRegistry = {
  // Navigation
  home: HomeIcon,
  briefcase: BriefcaseIcon,
  document: DocumentIcon,
  users: UsersIcon,
  chat: ChatBubbleLeftRightIcon,
  cpu: CpuChipIcon,
  cog: CogIcon,
  chart: ChartBarIcon,
  folder: FolderIcon,
  clipboard: ClipboardDocumentListIcon,
  
  // Actions
  search: MagnifyingGlassIcon,
  close: XMarkIcon,
  user: UserIcon,
  'chevron-down': ChevronDownIcon,
  'chevron-left': ChevronLeftIcon,
  logout: ArrowRightOnRectangleIcon,
  plus: PlusIcon,
  edit: PencilIcon,
  trash: TrashIcon,
  eye: EyeIcon,
  play: PlayIcon,
  pause: PauseIcon,
  duplicate: DocumentDuplicateIcon,
  
  // Status
  warning: ExclamationTriangleIcon,
  success: CheckCircleIcon,
  info: InformationCircleIcon,
  error: ExclamationTriangleIcon,
  clock: ClockIcon,
  bolt: BoltIcon
}

// Fallback icons (SVG strings)
const fallbackIcons: Record<string, string> = {
  home: '<svg fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>',
  briefcase: '<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2h2zm4-1a1 1 0 00-1 1v1h2V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>',
  document: '<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/></svg>',
  users: '<svg fill="currentColor" viewBox="0 0 20 20"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/></svg>',
  chat: '<svg fill="currentColor" viewBox="0 0 20 20"><path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"/><path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z"/></svg>',
  cpu: '<svg fill="currentColor" viewBox="0 0 20 20"><path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/></svg>',
  cog: '<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/></svg>'
}

// Computed properties
const iconComponent = computed(() => {
  return iconRegistry[props.name as keyof typeof iconRegistry]
})

const fallbackIcon = computed(() => {
  return props.fallback || fallbackIcons[props.name]
})

const iconClasses = computed(() => {
  const sizeClasses = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-8 h-8'
  }
  
  const classes = [sizeClasses[props.size as keyof typeof sizeClasses]]
  
  if (props.color) {
    classes.push(props.color)
  }
  
  return classes
})

// Error handling
const handleError = () => {
  hasError.value = true
  console.warn(`Icon "${props.name}" failed to load, using fallback`)
}

// Error handling removed for now
</script>

<style scoped>
.fallback-icon {
  @apply text-neutral-400;
}

.fallback-icon svg {
  @apply w-full h-full;
}
</style>