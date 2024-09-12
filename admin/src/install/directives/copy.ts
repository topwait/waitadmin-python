import feedback from '@/utils/feedback'
import useClipboard from 'vue-clipboard3'

const clipboard: string = 'data-clipboard-text'

export default {
    mounted: (el: HTMLElement, binding: any): void => {
        el.setAttribute(clipboard, binding.value)
        const { toClipboard } = useClipboard()

        el.onclick = (): void => {
            toClipboard(el.getAttribute(clipboard)!)
                .then((): void => {
                    feedback.msgSuccess('复制成功')
                })
                .catch((): void => {
                    feedback.msgError('复制失败')
                })
        }
    },
    updated: (el: HTMLElement, binding: any): void => {
        el.setAttribute(clipboard, binding.value)
    }
}
