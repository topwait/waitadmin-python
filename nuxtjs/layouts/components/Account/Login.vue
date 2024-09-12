<template>
    <div class="login-popup-container">
        <!-- 普通登录 -->
        <template v-if="meansChannel.includes(currentLogin)">
            <div v-if="meansChannel.length" class="pt-[20px] px-[20px]">
                <el-tabs v-model="currentLogin" class="tabs">
                    <el-tab-pane v-if="meansChannel.includes('account')" label="账号登录" name="account" />
                    <el-tab-pane v-if="meansChannel.includes('mobile')" label="验证码登录" name="mobile" />
                </el-tabs>
                <!-- 账号登录 -->
                <el-form v-if="currentLogin === 'account'" ref="formRef" size="large" :model="formData" :rules="formRules">
                    <el-form-item prop="account">
                        <el-input v-model="formData.account" placeholder="请输入账号/邮箱"/>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input
                            v-model="formData.password"
                            type="password"
                            show-password
                            placeholder="请输入密码"
                        />
                    </el-form-item>
                    <el-form-item class="additional">
                        <nuxt-link
                            class="cursor-pointer hover-opacity"
                            @click="appStore.setPopup(popupEnum.REGISTER)"
                        >
                            立即注册
                        </nuxt-link>
                        <span class="px-[8px]">|</span>
                        <nuxt-link
                            class="cursor-pointer hover-opacity"
                            @click="appStore.setPopup(popupEnum.FORGOT_PWD)"
                        >
                            忘记密码?
                        </nuxt-link>
                    </el-form-item>
                    <el-form-item>
                        <el-button
                            type="primary"
                            class="w-full"
                            :loading="isLock"
                            @click="onAccountLoginLock()"
                        >
                            登录
                        </el-button>
                    </el-form-item>
                </el-form>
                <!-- 短信登录 -->
                <el-form v-if="currentLogin === 'mobile'" ref="formRef" size="large" :model="formData" :rules="formRules">
                    <el-form-item prop="mobile">
                        <el-input v-model="formData.mobile" placeholder="请输入手机号">
                            <template #prepend>
                                <ElSelect model-value="+86" style="width: 80px">
                                    <ElOption label="+86" value="+86" />
                                </ElSelect>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="code">
                        <el-input v-model="formData.code" placeholder="请输入验证码">
                            <template #suffix>
                                <div class="flex justify-center leading-5 w-[90px] pl-2.5 border-l border-br">
                                    <verify-code ref="verifyCodeRef" @click-get="handleSendSms" />
                                </div>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item class="additional">
                        <nuxt-link
                            class="cursor-pointer hover-opacity"
                            @click="appStore.setPopup(popupEnum.REGISTER)"
                        >
                            立即注册
                        </nuxt-link>
                        <span class="px-[8px]">|</span>
                        <nuxt-link
                            class="cursor-pointer hover-opacity"
                            @click="appStore.setPopup(popupEnum.FORGOT_PWD)"
                        >
                            忘记密码?
                        </nuxt-link>
                    </el-form-item>
                    <el-form-item>
                        <el-button
                            type="primary"
                            class="w-full h-42"
                            :loading="isLock"
                            @click="onAccountLoginLock()"
                        >
                            登录
                        </el-button>
                    </el-form-item>
                </el-form>
            </div>
            <div v-if="oauthChannel.length" class="oauth">
                <el-divider>其它方式登录</el-divider>
                <div class="flex justify-center my-[30px]">
                    <icon
                        v-if="oauthChannel.includes('wx')"
                        name="svg-icon-Wechat"
                        size="42"
                        color="#00c800"
                        class="mx-10 cursor-pointer"
                        @click="currentLogin = 'wx'"
                    />
                </div>
            </div>
        </template>

        <!-- 微信登录 -->
        <template v-if="oauthChannel.includes(currentLogin)">
            <div v-if="oauthChannel.length" class="pt-[30px] px-[20px]">
                <div class="text-3xl font-semibold text-tx-regular text-center">微信扫一扫登录</div>
                <div class="flex flex-col items-center mt-[10px] mb-[25px]">
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
                                <div v-if="sanCodeStatus === 3">认证成功</div>
                            </div>
                        </div>
                    </div>
                    <template v-if="sanCodeStatus === 0">
                        <div class="mt-[10px]">微信扫码登录/注册</div>
                        <div class="mt-[18px] text-base text-tx-placeholder">首次扫码关注公众号后将自动注册新账号</div>
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
            <div v-if="meansChannel.length" class="oauth">
                <div class="flex justify-center items-center text-primary-default cursor-pointer hover-opacity">
                    <icon name="el-icon-Iphone" size="18" />
                    <div class="button" @click="currentLogin = meansChannel[0]">
                        <span class="ml-[6px]">账号登录</span>
                    </div>
                </div>
            </div>
        </template>

        <!-- 隐私协议 -->
        <div class="protocol">
            您登录或注册即同意
            <nuxt-link
                v-slot="{ href }"
                :to="`/policy/${policyEnum.SERVICE}`"
                custom
            >
                <a
                    :href="href"
                    target="_blank"
                    class="text-tx-regular cursor-pointer hover-opacity"
                >
                    《用户协议》
                </a>
            </nuxt-link>和
            <nuxt-link
                v-slot="{ href }"
                :to="`/policy/${policyEnum.PRIVACY}`"
                custom
            >
                <a
                    :href="href"
                    target="_blank"
                    class="text-tx-regular cursor-pointer hover-opacity"
                >
                    《隐私政策》
                </a>
            </nuxt-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { policyEnum, popupEnum } from '@/enums/app'
import { noticeEnum } from '~/enums/notice'
import useUserStore from '~/stores/user'
import useAppStore from '~/stores/app'
import loginApi from '~/api/login'
import appApi from '~/api/app'

const appStore = useAppStore()
const userStore = useUserStore()

// 登录配置
const currentLogin = ref(appStore.getLoginConfig.defaults)
const meansChannel = computed(() => (appStore.getLoginConfig || {}).means)
const oauthChannel = computed(() => (appStore.getLoginConfig || {}).oauth)

// 表单参数
const formData = reactive({
    password: '',
    account: '',
    mobile: '',
    code: ''
})

// 扫码登录
let timer: any = null
const sanCodeStatus = ref(0)  // 扫码状态: [0=等待扫码,1=扫码失败,2=扫码确认,3=扫码成功]
const sanQrCodeUrl = ref('')  // 二维码链接
const sanLoginKey = ref('')   // 登录密钥
const sanExpire = ref(0)      // 失效时间

// 表单验证
const formRef = shallowRef<FormInstance>()
const formRules: FormRules = {
    mobile: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        {
            pattern: /^((0\d{2,3}-\d{7,8})|(1[3584]\d{9}))$/,
            message: '请输入正确的手机号码',
            trigger: 'blur'
        },
    ],
    account: [{ required: true,  message: '请输入手机号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

/**
 * 发验证码
 */
const isSendIng = ref(false)
const verifyCodeRef = shallowRef()
const handleSendSms = async () => {
    if (!formData.mobile) {
        return feedback.msgError('请填写手机号')
    }
    if (isSendIng.value) {
        return feedback.msgError('操作频繁,请稍后再试')
    }
    await formRef.value?.validateField(['mobile']).then(async () => {
        isSendIng.value = true
        verifyCodeRef.value?.ing()
        await appApi.sendSms({
            scene: noticeEnum.LOGIN,
            mobile: formData.mobile
        }).then(() => {
            feedback.msgSuccess('发送成功')
            verifyCodeRef.value?.start()
        }).catch(() => {
            verifyCodeRef.value?.end()
        }).finally(() => {
            isSendIng.value = false
        })
    }).catch(() => {})
}

/**
 * 账号登录
 */
const { lockFn:onAccountLoginLock, isLock } = useLockFn(async () => {
    const scene = currentLogin.value
    let params = {}
    switch(scene) {
        case 'account':
            params = {
                scene: scene,
                account: formData.account,
                password: formData.password
            }
            break
        case 'mobile':
            params = {
                scene: scene,
                mobile: formData.mobile,
                code: formData.code
            }
    }

    await loginApi.login(params).then(async (res) => {
        feedback.msgSuccess('登录成功')
        userStore.login(res.token)
        await userStore.getUser()
        appStore.setPopup(popupEnum.NULL)
        setTimeout(() => {
            location.reload()
        }, 800)
    }).catch(() => {})
})

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

watch(currentLogin, () => {
    sanCodeStatus.value = 0
    sanQrCodeUrl.value = ''
    sanLoginKey.value = ''
    sanExpire.value = 0
    if (timer !== null && timer !== undefined) {
        clearInterval(timer)
    }

    if (currentLogin.value === 'wx') {
        getOaLoginQrCode()
    }
}, { immediate: true })

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
</script>

<style lang="scss">
.login-popup-container {
    width: 390px;
    .tabs {
        padding-bottom: 10px;
        .el-tabs__item{
            font-size: 18px;
            font-weight: 600;
            color: var(--el-text-color-regular);
            &.is-active,
            &:hover {
                color: var(--el-color-primary);
            }
        }
        .el-tabs__nav-wrap::after {
            background-color: var(--el-border-color-light);
        }
    }

    .el-form {
        .el-input__inner { height: 46px; }
        .el-select__wrapper { box-shadow: none !important; }
        .additional .el-form-item__content {
            display: flex;
            justify-content: flex-end;
            line-height: 18px;
        }
    }

    .oauth {
        padding: 0 25px;
        .el-divider__text.is-center {
            font-size: 12px;
            color: var(--el-text-color-secondary);
        }
    }

    .protocol {
        padding: 10px;
        margin-top: 20px;
        font-size: 13px;
        color: var(--el-text-color-secondary);
        background-color: var(--el-bg-color-page);
        border-radius: 4px;
    }
}
</style>