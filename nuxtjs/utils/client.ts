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
     */
    isMobile(): boolean {
        return isMobileJs().any
    },

    /**
     * 是否为微信环境
     */
    isWeixin(): boolean {
        return /MicroMessenger/i.test(navigator.userAgent)
    },

    /**
     * 取当前的客户端
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
     */
    handleClientCallback(callbacks: ClientCallbacks) {
        const c = ClientEnum[this.getClient()]
        const callback = callbacks[c as keyof ClientCallbacks] || function () { }
        return callback()
    }
}

export default clientUtil
