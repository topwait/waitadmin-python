import { ref } from 'vue'

/**
 * 防止函数被重复执行 (防抖)
 *
 * @param fn
 * @author zero
 */
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
