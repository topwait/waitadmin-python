<template>
    <div class="pt-[30px] px-[20px]">
        <div class="text-3xl font-semibold text-tx-regular text-center">
            微信扫一扫登录
        </div>
        <div class="flex flex-col items-center mt-[10px] mb-[25px]">
            <div
                v-if="!isAgreement"
                class="flex items-center justify-center
                       w-[206px] h-[206px] bg-light text-primary"
            >
                <icon name="el-icon-WarningFilled" />
                <span class="ml-1">请阅读并同意协议</span>
            </div>

            <div v-else v-loading="!sanQrCodeUrl" class="relative w-[206px] h-[206px]">
                <img
                    v-if="sanQrCodeUrl"
                    :src="sanQrCodeUrl"
                    alt="qr"
                    style="width: 214px; height: 214px;"
                />
                <div
                    v-if="sanCodeStatus !== 0"
                    class="absolute left-0 top-0 w-full h-full bg-overlay cursor-pointer"
                    @click="onRefreshOrCode()"
                >
                    <div class="h-full flex flex-col justify-center items-center text-white">
                        <div v-if="sanCodeStatus === 1">点击刷新</div>
                        <div v-if="sanCodeStatus === 2">等待确认</div>
                        <div v-if="sanCodeStatus === 3">认证成功</div>
                    </div>
                </div>
            </div>
            <template v-if="sanCodeStatus === 0">
                <div class="mt-[10px]">微信扫码登录/注册</div>
                <div class="mt-[18px] text-base text-tx-placeholder">
                    首次扫码关注公众号后将自动注册新账号
                </div>
            </template>
            <template v-if="sanCodeStatus === 1">
                <div class="mt-[10px] text-error">二维码失效</div>
                <div class="mt-[18px] text-base">请在点击二维码刷新</div>
            </template>
            <template v-if="sanCodeStatus === 2">
                <div class="mt-[10px] text-error">扫码成功</div>
                <div class="mt-[18px] text-base">请在微信公众号中确认登录</div>
            </template>
            <template v-if="sanCodeStatus === 3">
                <div class="mt-[10px] text-error">登录成功</div>
                <div class="mt-[18px] text-base">请耐心等待页面进行跳转</div>
            </template>
        </div>
    </div>
</template>

<script setup lang="ts">
import { popupEnum } from '@/enums/app'
import useUserStore from '@/stores/user'
import useAppStore from '@/stores/app'
import loginApi from '@/api/login'

const props = defineProps({
    protocol: {
        type: Boolean,
        default: false
    }
})

const appStore = useAppStore()
const userStore = useUserStore()

// 是否同意协议
const isAgreement = ref<boolean>(props.protocol)

// 扫码登录信息
let timer: any = null
const sanCodeStatus = ref<number>(0)  // 扫码状态: [0=等待扫码,1=扫码失败,2=扫码确认,3=扫码成功]
const sanQrCodeUrl = ref<string>('')  // 二维码链接
const sanLoginKey = ref<string>('')   // 登录密钥
const sanExpire = ref<number>(0)      // 失效时间

/**
 * 刷新二维码
 */
const onRefreshOrCode = () => {
    if (sanCodeStatus.value === 1) {
        getOaLoginQrCode()
    }
}

/**
 * 公众号登录
 */
const getOaLoginQrCode = async () => {
    sanQrCodeUrl.value = ''
    sanCodeStatus.value = 0
    const data = await loginApi.oaLoginQr('login')
    data.expire_seconds = parseInt(String(data.expire_seconds || 120))
    sanQrCodeUrl.value = data.url
    sanLoginKey.value = data.key
    sanExpire.value = data.expire_seconds

    if (timer) {
        clearInterval(timer)
        timer = null
    }

    timer = setInterval(async () => {
        if (sanExpire.value) {
            sanExpire.value = sanExpire.value - 1
            const result = await loginApi.oaTicket(data.key)
            if (result?.token && result.status === 3) {
                clearInterval(timer)
                timer = null
                sanCodeStatus.value = 3
                userStore.login(result.token)
                await userStore.getUser()
                setTimeout(() => {
                    appStore.setPopup(popupEnum.NULL)
                    location.reload()
                }, 1800)
            } else if (result.status === 2) {
                sanCodeStatus.value = result.status
            } else if (result.status !== 0) {
                clearInterval(timer)
                timer = null
            }
        } else {
            sanCodeStatus.value = 1
            clearInterval(timer)
            timer = null
        }
    }, 2000)
}

watch(
    () => props.protocol,
    async (val: boolean) => {
        isAgreement.value = val
        if (val) {
            await getOaLoginQrCode()
        }
    }, { immediate: true }
)

onBeforeUnmount(() => {
    if (timer !== null) {
        clearInterval(timer)
    }
})
</script>
