import { Alipay } from './alipay'
import { Wxpay } from './wxpay'
import { Pay } from './pay'

// 支付方式
enum PayWayEnum {
    WXPAY = 2,
    ALIPAY = 3
}

// 注入微信支付
const wxpay: Wxpay = new Wxpay()
Pay.inject('WXPAY', wxpay)

// 注入支付宝支付
const alipay: Alipay = new Alipay()
Pay.inject('ALIPAY', alipay)

const pay: Pay = new Pay()
export { pay, PayWayEnum }
