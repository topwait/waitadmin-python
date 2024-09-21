export function useLockFn(fn: (...args: any[]) => Promise<any>, delay: number = 0) {
    const isLock: globalThis.Ref<boolean> = ref(false)
    const lockFn = async (...args: any[]): Promise<any> => {
        if (isLock.value) {
            return
        }
        isLock.value = true
        try {
            const res = await fn(...args)
            if (delay) {
                setTimeout(() => {
                    isLock.value = false
                }, delay)
            } else {
                isLock.value = false
            }
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
