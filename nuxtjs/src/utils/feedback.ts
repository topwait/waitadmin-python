import type { LoadingInstance } from 'element-plus/es/components/loading/src/loading'
import type { MessageBoxData, ElMessageBoxOptions } from 'element-plus'
import {
    ElMessage,
    ElMessageBox,
    ElNotification,
    ElLoading
} from 'element-plus'


export class Feedback {
    private loadingInstance: LoadingInstance | null = null
    static instance: Feedback | null = null

    static getInstance(): Feedback {
        return this.instance ?? (this.instance = new Feedback())
    }

    /**
     * 消息提示
     *
     * @param {string} msg
     * @returns {void}
     */
    msg(msg: string): void {
        ElMessage.info(msg)
    }

    /**
     * 错误消息
     *
     * @param {string} msg
     * @returns {void}
     */
    msgError(msg: string): void {
        ElMessage.error(msg)
    }

    /**
     * 成功消息
     *
     * @param {string} msg
     * @returns {void}
     */
    msgSuccess(msg: string): void {
        ElMessage.success(msg)
    }

    /**
     * 警告消息
     *
     * @param {string} msg
     * @returns {void}
     */
    msgWarning(msg: string): void {
        ElMessage.warning(msg)
    }

    /**
     * 弹出提示
     *
     * @param {string} msg
     * @returns {void}
     */
    alert(msg: string): void {
        ElMessageBox.alert(msg, '系统提示').then((): void => { })
    }

    /**
     * 错误提示
     *
     * @param {string} msg
     * @returns {void}
     */
    alertError(msg: string): void {
        ElMessageBox.alert(msg, '系统提示', { type: 'error' }).then((): void => { })
    }

    /**
     * 成功提示
     *
     * @param {string} msg
     * @returns {void}
     */
    alertSuccess(msg: string): void {
        ElMessageBox.alert(msg, '系统提示', { type: 'success' }).then((): void => { })
    }

    /**
     * 警告提示
     *
     * @param {string} msg
     * @returns {void}
     */
    alertWarning(msg: string): void {
        ElMessageBox.alert(msg, '系统提示', { type: 'warning' }).then((): void => { })
    }

    /**
     * 通知提示
     *
     * @param {string} msg
     * @returns {void}
     */
    notify(msg: string): void {
        ElNotification.info(msg)
    }

    /**
     * 错误通知
     *
     * @param {string} msg
     * @returns {void}
     */
    notifyError(msg: string): void {
        ElNotification.error(msg)
    }

    /**
     * 成功通知
     *
     * @param {string} msg
     * @returns {void}
     */
    notifySuccess(msg: string): void {
        ElNotification.success(msg)
    }

    /**
     * 警告通知
     *
     * @param {string} msg
     * @returns {void}
     */
    notifyWarning(msg: string): void {
        ElNotification.warning(msg)
    }

    /**
     * 确认窗体
     *
     * @param {string} msg
     * @returns {Promise<MessageBoxData>}
     */
    confirm(msg: string): Promise<MessageBoxData> {
        return ElMessageBox.confirm(msg, '温馨提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
    }

    /**
     * 提交内容
     *
     * @param {string} content
     * @param {string} title
     * @param {ElMessageBoxOptions} options
     * @returns {Promise<MessageBoxData>}
     */
    prompt(content: string, title: string, options?: ElMessageBoxOptions): Promise<MessageBoxData> {
        return ElMessageBox.prompt(content, title, {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            ...options
        })
    }

    /**
     * 打开全局loading
     *
     * @param {string} msg
     * @returns {void}
     */
    loading(msg: string): void {
        this.loadingInstance = ElLoading.service({
            lock: true,
            text: msg
        })
    }

    /**
     * 关闭全局loading
     */
    closeLoading(): void {
        this.loadingInstance?.close()
    }
}

const feedback: Feedback = Feedback.getInstance()
export default feedback
