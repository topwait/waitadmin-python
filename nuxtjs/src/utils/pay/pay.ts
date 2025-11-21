import { PayWayEnum } from '.'

export interface PayOptions {
    // 调用类型: [qr=二维码,window=窗口]
    aliType?: string
    // 订单的ID
    orderId: string | number
    // 支付方式
    payWay: PayWayEnum
    // 支付场景
    attach: string
    // 支付配置
    config: any
}

export class Pay {
    [x: string]: any
    // 维护模块名单
    private static modules = new Map()
    static inject(name: string, module: any) {
        this.modules.set(name, module)
    }

    // 注入支付方式
    constructor() {
        for (const [name, module] of Pay.modules.entries()) {
            module.init(name, this)
        }
    }

    // 调用拉起支付
    async run(options: PayOptions) {
        try {
            // @ts-ignore
            const module = this[PayWayEnum[options.payWay]]
            if (!module) {
                return Promise.reject(`can not find pay way ${options.payWay}`)
            }
            return await module.run(options)
        } catch (error) {
            return Promise.reject(error)
        }
    }
}
