import { useClipboard } from '@vueuse/core'
import { ElMessage } from 'element-plus'

/**
 * 复制内容函数
 *
 * @author zero
 */
export const useCopy = () => {
    const copy = async (text: string, message: string = '复制成功') => {
        const { copy } = useClipboard({ source: text })
        try {
            if (navigator.clipboard) {
                setTimeout(async (): Promise<void> => {
                    await copy(text)
                }, 0)
            } else {
                const textarea = document.createElement('textarea')
                textarea.value = text
                document.body.appendChild(textarea)
                textarea.select()
                document.execCommand('copy')
                document.body.removeChild(textarea)
            }
            ElMessage.success({ message: message })
        } catch {
            ElMessage.error({ message: '复制失败' })
        }
    }
    return {
        copy
    }
}
