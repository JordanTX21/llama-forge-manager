<script setup lang="ts">
import { useToastStore } from '@/stores/toast.store'
import { storeToRefs } from 'pinia'
import { CheckCircle, AlertTriangle, XCircle, Info, X } from '@lucide/vue'

const store = useToastStore()
const { toasts } = storeToRefs(store)

const iconMap = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertTriangle,
  info: Info
} as const
</script>

<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div v-for="t in toasts" :key="t.id" class="toast-item" :class="`toast--${t.type}`">
          <div class="toast-icon">
            <component :is="iconMap[t.type]" class="w-[18px] h-[18px]" />
          </div>
          <span class="toast-message">{{ t.message }}</span>
          <button class="toast-close" @click="store.remove(t.id)">
            <X class="w-3.5 h-3.5" />
          </button>
          <!-- Progress bar -->
          <div class="toast-progress" :style="{ animationDuration: `${t.duration}ms` }"></div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 1.25rem;
  right: 1.25rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  max-width: 400px;
  pointer-events: none;
}

.toast-item {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 0.875rem;
  border: 1px solid;
  backdrop-filter: blur(16px) saturate(1.8);
  -webkit-backdrop-filter: blur(16px) saturate(1.8);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.04) inset;
  position: relative;
  overflow: hidden;
  min-width: 300px;
}

.toast-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-message {
  flex: 1;
  font-size: 0.8125rem;
  font-weight: 500;
  line-height: 1.4;
}

.toast-close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 0.375rem;
  opacity: 0.5;
  transition: opacity 0.2s, background 0.2s;
  cursor: pointer;
  background: none;
  border: none;
  color: inherit;
}
.toast-close:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.08);
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 100%;
  animation: shrink linear forwards;
  transform-origin: left;
}

@keyframes shrink {
  from { transform: scaleX(1); }
  to { transform: scaleX(0); }
}

/* ── Type Variants ── */
.toast--success {
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.25);
  color: #86efac;
}
.toast--success .toast-icon { color: #22c55e; }
.toast--success .toast-progress { background: #22c55e; }

.toast--error {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.25);
  color: #fca5a5;
}
.toast--error .toast-icon { color: #ef4444; }
.toast--error .toast-progress { background: #ef4444; }

.toast--warning {
  background: rgba(234, 179, 8, 0.1);
  border-color: rgba(234, 179, 8, 0.25);
  color: #fde68a;
}
.toast--warning .toast-icon { color: #eab308; }
.toast--warning .toast-progress { background: #eab308; }

.toast--info {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.25);
  color: #93c5fd;
}
.toast--info .toast-icon { color: #3b82f6; }
.toast--info .toast-progress { background: #3b82f6; }

/* ── Transitions ── */
.toast-enter-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 1, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(80px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(80px) scale(0.95);
}
.toast-move {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
