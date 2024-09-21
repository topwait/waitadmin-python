<template>
    <div class="w-[360px] px-2">
        <div class="font-semibold mb-4">
            {{ users?.is_wechat ? '换绑微信' : '绑定微信' }}
        </div>
        <div class="flex flex-col items-center">
            <div v-loading="!sanQrCodeUrl" class="relative w-[206px] h-[206px]">
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
                        <div v-if="sanCodeStatus === 3">绑定成功</div>
                    </div>
                </div>
            </div>
            <template v-if="sanCodeStatus === 0">
                <div class="mt-[10px]">使用手机微信扫码绑定</div>
                <div class="mt-[18px] text-base text-tx-placeholder">绑定后可使用微信扫码登录</div>
            </template>
            <template v-if="sanCodeStatus === 1">
                <div class="mt-[10px] text-error">二维码失效</div>
                <div class="mt-[18px] text-base">请在点击二维码刷新</div>
            </template>
            <template v-if="sanCodeStatus === 2">
                <div class="mt-[10px] text-error">扫码成功</div>
                <div class="mt-[18px] text-base">请在微信公众号中确认绑定</div>
            </template>
            <template v-if="sanCodeStatus === 3">
                <div class="mt-[10px] text-error">绑定成功</div>
                <div class="mt-[18px] text-base">恭喜您绑定微信成功</div>
            </template>
        </div>
    </div>
</template>

<script setup lang="ts">
import useUserStore from '~/stores/user'
import useAppStore from '~/stores/app'
import loginApi from '~/api/login'

const userStore = useUserStore()
const appStore = useAppStore()

// 用户信息
const { users } = toRefs(userStore)

// 微信扫码
let timer: any = null
const sanCodeStatus = ref(0)  // 扫码状态: [0=等待扫码,1=扫码失败,2=扫码确认,3=扫码成功]
const sanQrCodeUrl = ref('')  // 二维码链接
const sanLoginKey = ref('')   // 登录密钥
const sanExpire = ref(0)      // 失效时间

/**
 * 微信二维码
 */
const getOaLoginQrCode = async () => {
    sanQrCodeUrl.value = ''
    sanCodeStatus.value = 0
    const data = await loginApi.oaLoginQr('bind')
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
            if (result.status === 3) {
                clearInterval(timer)
                timer = null
                sanCodeStatus.value = 3
                await userStore.getUser()
            } else if (result.status === 2) {
                sanCodeStatus.value = result.status
            } else if (result.status !== 0) {
                sanCodeStatus.value = 1
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

/**
 * 刷新二维码
 */
const onRefreshOrCode = async () => {
    await getOaLoginQrCode()
}

const { popupType } = toRefs(appStore)
watch(popupType, () => {
    if (timer !== null) {
        clearInterval(timer)
    }
})

onBeforeUnmount(() => {
    if (timer !== null) {
        clearInterval(timer)
    }
})

onMounted(async () => {
    await getOaLoginQrCode()
})
</script>

<style lang="scss">
.forgot-popup-container {
    width: 390px;
    .el-form {
        .el-input__inner { height: 46px; }
    }
}
</style>