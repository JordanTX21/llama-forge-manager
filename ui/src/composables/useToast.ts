import { useToastStore, type ToastType } from '@/stores/toast.store'

export function useToast() {
  const store = useToastStore()

  const toast = (message: string, type: ToastType = 'info', duration = 4000) => {
    store.add(message, type, duration)
  }

  const success = (message: string, duration?: number) => toast(message, 'success', duration)
  const error = (message: string, duration?: number) => toast(message, 'error', duration)
  const warning = (message: string, duration?: number) => toast(message, 'warning', duration)
  const info = (message: string, duration?: number) => toast(message, 'info', duration)

  return { toast, success, error, warning, info }
}
