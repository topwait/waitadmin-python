<template>
    <div v-if="rechargeConfig.status">
        <el-card class="!border-none" shadow="never">
            <div class="grid grid-cols-3 md:grid-cols-3 gap-4">
                <div class="flex flex-col items-center justify-center">
                    <div class="font-medium text-[25px] text-primary-default">
                        {{ userInfo.balance }}
                    </div>
                    <div class="mt-[4px] font-bold">当前余额</div>
                </div>
            </div>
        </el-card>

        <el-card class="!border-none mt-4" shadow="never">
            <div class="text-xl font-medium mb-[20px]">选择套餐</div>
            <div class="packages">
                <div
                    v-for="(item, index) in packages"
                    :key="index"
                    class="item"
                    :class="{ active: index === currentIndex }"
                    @click="currentIndex = index"
                >
                    <span v-if="item.give_money" class="tips">
                        赠送{{ item.give_money }}元
                    </span>
                    <p class="name">{{ item.name }}</p>
                    <p class="money">{{ item.money }}</p>
                    <div class="footer">¥{{ item.money }}</div>
                    <div v-if="index === currentIndex" class="select-icon">
                        <icon class="el-icon-select" name="el-icon-Select" />
                    </div>
                </div>
                <div
                    class="item"
                    :class="{ active: -1 === currentIndex }"
                    @click="currentIndex = -1"
                >
                    <p class="name">自定义充值</p>
                    <p class="money">
                        <el-input v-model="money" />
                    </p>
                    <div class="footer">输入自定义金额</div>
                    <div v-if="currentIndex === -1" class="select-icon">
                        <icon class="el-icon-select" name="el-icon-Select" />
                    </div>
                </div>
            </div>
        </el-card>

        <el-card class="!border-none mt-4" shadow="never">
            <div class="text-xl font-medium mb-[20px]">支付方式</div>
            <PaymentSelect v-model="payWay" from="recharge"/>
        </el-card>

        <el-card class="!border-none mt-4" shadow="never">
            <div class="flex justify-between">
                <div>
                    实付金额:
                    <Price
                        :content="currentIndex === -1 ? money : currentPackage.money"
                        main-size="24px"
                        minor-size="14px"
                        color="#FF7021"
                    />
                </div>
                <ElButton
                    type="primary"
                    size="large"
                    style="padding: 0 54px;"
                    :loading="isLock"
                    @click="payNow"
                >
                    立即充值
                </ElButton>
            </div>
        </el-card>
    </div>

    <el-card v-else class="!border-none h-full" shadow="never">
        <el-empty
            description="充值已关闭"
            :image-size="200"
        />
    </el-card>
</template>

<script setup lang="ts">
import { pay, PayWayEnum } from '~/utils/pay'
import useAppStore from '~/stores/app'
import useUserStore from '~/stores/user'
import paymentApi from '@/api/payment'
import rechargeApi from '@/api/recharge'

const appStore = useAppStore()
const userStore = useUserStore()
const userInfo = computed(() => userStore.users)
const rechargeConfig = computed(() => appStore.getRechargeConfig)

const money = ref<number>(100)
const payWay = ref<number>(PayWayEnum.WXPAY)
const packages = ref<RechargePackageResponse[]>([])

// 充值套餐
const currentIndex = ref(0)
const currentPackage = computed(() => {
    return packages.value[currentIndex.value] || {}
})

// 发起支付
const {lockFn: payNow, isLock} = useLockFn(async () => {
    // 验证订单
    if (currentIndex.value === -1) {
        if (money.value < rechargeConfig.value.min_recharge) {
            return feedback.msgError('充值金额不能少于: ' + money.value)
        }
    }

    // 创建订单
    const packageId = parseInt(currentPackage.value?.id || '0')
    const amountVal = packageId ? currentPackage.value?.money : money.value
    const orderInfo = await rechargeApi.place({
        money: amountVal,
        package_id: packageId
    })

    // 预付下单
    const payInfo = await paymentApi.prepay({
        order_id: orderInfo.order_id,
        pay_way: payWay.value,
        attach: 'recharge'
    })

    // 拉起支付
    await pay.run({
        payWay: payWay.value,
        orderId: orderInfo.order_id,
        config: payInfo,
        attach: 'recharge'
    }).then(async () => {
        await userStore.getUser()
        feedback.alertSuccess('支付成功')
    }).catch(() => {})
})

onMounted(async () => {
    packages.value = await rechargeApi.package()
})
</script>

<style scoped lang="scss">
.packages {
    display: flex;
    flex-wrap: wrap;
    .item {
        position: relative;
        width: 204px;
        height: 136px;
        margin: 0 15px 15px;
        text-align: center;
        cursor: pointer;
        border: 2px solid var(--el-color-primary-light-5);
        border-radius: 8px;
        &.active,
        &:hover {
            background-color: var(--el-color-primary-light-9);
            border-color: var(--el-color-primary);
        }
        .tips {
            position: absolute;
            top: -2px;
            left: -2px;
            height: 24px;
            padding: 0 4px;
            font-size: 13px;
            line-height: 24px;
            color: var(--color-white);
            background: linear-gradient(90deg, #fc5531, #fc1944);
            border-radius: 6px 0 8px;
        }
        .name {
            position: relative;
            z-index: 2;
            height: 22px;
            margin: 25px 0 10px;
            font-size: 16px;
            font-weight: 700;
            line-height: 22px;
            color: var(--el-text-color-regular);
        }
        .money {
            font-size: 24px;
            font-weight: 700;
            line-height: 32px;
            color: var(--el-color-primary);
        }
        .footer {
            position: absolute;
            bottom: 0;
            z-index: 2;
            width: 100%;
            height: 32px;
            overflow: hidden;
            font-size: 13px;
            font-weight: 600;
            line-height: 32px;
            color: var(--el-color-primary);
            background-color: var(--el-color-primary-light-7);
            border-radius: 0 0 6px 6px;
        }
        .select-icon {
            position: absolute;
            right: -1px;
            bottom: -1px;
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 26px;
            height: 26px;
            clip-path: polygon(0 100%, 100% 0, 100% 100%);
            color: var(--color-white);
            background-color: var(--el-color-primary);
            :deep() .el-icon-select {
                transform: translate(35%, 35%);
                transform-origin: center center;
            }
        }
        :deep(.el-input__wrapper) {
            text-align: center;
            background-color: unset;
            box-shadow: none;
            .el-input__inner {
                font-size: 24px;
                font-weight: 700;
                color: var(--el-color-primary);
                text-align: center;
            }
        }
    }
}
</style>
