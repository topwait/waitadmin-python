import isMobileJs from 'ismobilejs'
import { ClientEnum } from '@/enums/client'

interface ClientCallbacks {
    PC?(): any
    H5?(): any
    WEIXIN_OA?(): any
}

const clientUtil = {
    /**
     * 是否为手机环境
     *
     * @returns {boolean}
     * @author zero
     */
    isMobile(): boolean {
        return isMobileJs().any
    },

    /**
     * 是否为微信环境
     *
     * @returns {boolean}
     * @author zero
     */
    isWeixin(): boolean {
        return /MicroMessenger/i.test(navigator.userAgent)
    },

    /**
     * 取当前的客户端
     *
     * @returns {number}
     * @author zero
     */
    getClient(): number {
        if (this.isMobile()) {
            if (this.isWeixin()) {
                return ClientEnum.OA
            }
            return ClientEnum.H5
        }
        return ClientEnum.PC
    },

    /**
     * 根据客户端执行
     *
     * @returns {any}
     * @author zero
     */
    handleClientCallback(callbacks: ClientCallbacks): any {
        const c: string | undefined = ClientEnum[this.getClient()]
        const callback = callbacks[c as keyof ClientCallbacks] || function (): void { }
        return callback()
    }
}

export default clientUtil
