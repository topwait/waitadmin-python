import { Alipay } from './alipay'
import { Wxpay } from './wxpay'
import { Pay } from './pay'

// 支付方式
enum PayWayEnum {
    WXPAY = 2,
    ALIPAY = 3
}

// 注入微信支付
const wxpay = new Wxpay()
Pay.inject(PayWayEnum[2], wxpay)

// 注入支付宝支付
const alipay = new Alipay()
Pay.inject(PayWayEnum[3], alipay)

const pay = new Pay()
export { pay, PayWayEnum }
