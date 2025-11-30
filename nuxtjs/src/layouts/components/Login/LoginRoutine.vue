<template>
    <div class="routine-login-form">
        <!-- 选项卡 -->
        <el-tabs v-model="currentLogin" class="tabs">
            <el-tab-pane
                v-if="usableChannel.includes('account')"
                name="account"
                label="账号登录"
            />
            <el-tab-pane
                v-if="usableChannel.includes('mobile')"
                name="mobile"
                label="验证码登录"
            />
        </el-tabs>

        <!-- 登录表单 -->
        <el-form
            ref="formRef"
            size="large"
            :model="formData"
            :rules="formRules"
        >
            <!-- 账号登录表单 -->
            <template v-if="currentLogin === 'account'">
                <el-form-item prop="account">
                    <el-input v-model="formData.account" placeholder="请输入账号"/>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        v-model="formData.password"
                        type="password"
                        show-password
                        placeholder="请输入密码"
                    />
                </el-form-item>
            </template>

            <!-- 手机短信表单 -->
            <template v-if="currentLogin === 'mobile'">
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
            </template>

            <!-- 附加工具 -->
            <el-form-item class="additional">
                <nuxt-link
                    class="cursor-pointer hover:opacity-80"
                    @click="appStore.setPopup(popupEnum.REGISTER)"
                >
                    立即注册
                </nuxt-link>
                <span class="px-[8px]">|</span>
                <nuxt-link
                    class="cursor-pointer hover:opacity-80"
                    @click="appStore.setPopup(popupEnum.FORGOT_PWD)"
                >
                    忘记密码?
                </nuxt-link>
            </el-form-item>

            <!-- 登录按钮 -->
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
    </div>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { noticeEnum } from '@/enums/notice'
import { popupEnum } from '@/enums/app'
import useUserStore from '@/stores/user'
import useAppStore from '@/stores/app'
import loginApi from '@/api/login'
import appApi from '@/api/app'

const props = defineProps({
    protocol: {
        type: Boolean,
        default: false
    }
})

const appStore = useAppStore()
const userStore = useUserStore()

// 登录配置参数
const config = appStore.getLoginConfig.pc

// 是否同意协议
const isAgreement = ref<boolean>(props.protocol)

// 当前登录方式
const currentLogin = ref<string>(config?.default_method)

// 可用登录渠道
const usableChannel = ref<string[]>(config?.usable_channel)

// 表单参数
const formData = reactive<{
    account: string;
    password: string;
    mobile: string;
    code: string;
}>({
    // 账号登录参数
    account: '',
    password: '',
    // 短信登录参数
    mobile: '',
    code: ''
})

// 表单验证
const formRef = shallowRef<FormInstance>()
const formRules: FormRules = {
    mobile: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        {
            pattern: /^((0\d{2,3}-\d{7,8})|(1[3584]\d{9}))$/,
            message: '请输入正确的手机号码',
            trigger: 'blur'
        }
    ],
    code: [
        { required: true, message: '请输入验证码', trigger: 'blur' }
    ],
    account: [
        { required: true,  message: '请输入手机号', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入登录密码', trigger: 'blur' }
    ]
}

/**
 * 发验证码
 */
const isSmsSending = ref<boolean>(false)
const verifyCodeRef = shallowRef()
const handleSendSms = async () => {
    if (!isAgreement.value) {
        feedback.msgError('请阅读《服务协议》与《隐私协议》')
        return
    }
    if (!formData.mobile) {
        feedback.msgError('请填写手机号')
        return
    }
    if (isSmsSending.value) {
        feedback.msgError('操作频繁,请稍后再试')
        return
    }
    await formRef.value?.validateField(['mobile']).then(async () => {
        isSmsSending.value = true
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
            isSmsSending.value = false
        })
    }).catch(() => {})
}

/**
 * 账号登录
 */
const { lockFn:onAccountLoginLock, isLock } = useLockFn(async () => {
    if (!isAgreement.value) {
        feedback.msgError('请阅读《服务协议》与《隐私协议》')
        return
    }

    let action: any = null
    if (currentLogin.value === 'account') {
        action = loginApi.accountLogin({
            account: formData.account,
            password: formData.password
        })
    } else {
        action = loginApi.mobileLogin({
            mobile: formData.mobile,
            code: formData.code
        })
    }

    await action.then(async (res: LoginResultResponse) => {
        feedback.msgSuccess('登录成功')
        userStore.login(res.token)
        await userStore.getUser()
        appStore.setPopup(popupEnum.NULL)
        setTimeout(() => {
            location.reload()
        }, 800)
    }).catch(() => {})
})

watch(
    () => props.protocol,
    (val: boolean) => {
        isAgreement.value = val
    }
)
</script>

<style lang="scss">
.routine-login-form {
    padding: 20px 20px 0;
    // 选项卡样式
    .tabs {
        padding-bottom: 10px;

        .el-tabs__item {
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

    // 表单样式
    .el-form {
        .el-input__inner {
            height: 46px;
        }

        .el-select__wrapper {
            box-shadow: none !important;
        }

        .additional .el-form-item__content {
            display: flex;
            justify-content: flex-end;
            line-height: 18px;
        }
    }
}
</style>
