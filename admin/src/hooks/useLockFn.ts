import { ref } from 'vue'

export function useLockFn(fn: (...args: any[]) => Promise<any>): any {
    const isLock = ref(false)
    const lockFn = async (...args: any[]): Promise<any> => {
        if (isLock.value) {
            return
        }
        isLock.value = true
        try {
            const res = await fn(...args)
            isLock.value = false
            return res
        } catch (e) {
            isLock.value = false
            throw e
        }
    }
    return {
        isLock,
        lockFn
    }
}
