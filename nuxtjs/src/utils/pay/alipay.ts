import VueQr from 'vue-qr/src/packages/vue-qr.vue'
import type { MessageBoxData } from 'element-plus'
import type { PayOptions } from './pay'
import { createVNode } from 'vue'
import clientUtil from '@/utils/client'
import paymentApi from '@/api/payment'

export class Alipay {
    init(name: number, pay: any): void {
        pay[name] = this
    }

    run(options: PayOptions) {
        return new Promise((resolve, reject): void => {
            clientUtil.handleClientCallback({
                PC: (): void => {
                    if (options.aliType === 'window') {
                        const url = options.config
                        window.open(url, '_self')
                    } else {
                        this.sanCodePay(options, resolve, reject)
                    }
                },
                H5: (): void => {
                    window.open(options.config, '_self')
                }
            })
        })
    }

    sanCodePay(options: PayOptions, resolve: any, reject: any): void {
        const { start, end } = usePolling(
            async (): Promise<void> => {
                const { status } = await paymentApi.listen({
                    order_id: parseInt(String(options.orderId)),
                    attach: options.attach
                })
                if (status === 1) {
                    resolve('success')
                    ElMessageBox.close()
                    end()
                }
            },
            {
                key: 'payment',
                totalTime: 300 * 1000,
                callback: () => {
                    reject('支付超时!')
                    ElMessageBox.close()
                    feedback.alertWarning('支付超时！')
                }
            }
        )
        start()
        this.showQrCode(options.config).catch((): void => {
            end()
            reject('取消支付')
        })
    }

    async showQrCode(options: any): Promise<MessageBoxData> {
        const qrCode = createVNode(VueQr as any, {
            text: options,
            size: 160,
            dotScale: 1,
            margin: 0,
            style: {
                margin: '20px auto'
            }
        })
        const title = createVNode(
            'div',
            {
                style: {
                    fontSize: '16px',
                    color: '#333'
                }
            },
            '请使用支付宝扫一扫'
        )
        const tips1 = createVNode('div', null, '支付成功后自动关闭窗口')
        const tips2 = createVNode(
            'div',
            {
                style: {
                    marginTop: '10px'
                }
            },
            '如遇到支付问题，请联系客服解决'
        )
        return ElMessageBox({
            title: '支付宝支付',
            showConfirmButton: false,
            closeOnClickModal: false,
            center: true,
            message: createVNode(
                'div',
                {
                    style: {
                        'text-align': 'center'
                    }
                },
                [title, qrCode, tips1, tips2]
            )
        })
    }
}
