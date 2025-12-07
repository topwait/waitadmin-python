<template>
    <div class="register-popup-container">
        <!-- 注册账号 -->
        <div v-if="usableRegister.length" class="pt-[20px] px-[20px]">
            <el-tabs v-model="currentRegister" class="tabs">
                <el-tab-pane
                    v-if="usableRegister.includes('account')"
                    label="账号注册"
                    name="account"
                    @click="currentRegister = 'account'"
                />
                <el-tab-pane
                    v-if="usableRegister.includes('mobile')"
                    label="手机号注册"
                    name="mobile"
                    @click="currentRegister = 'mobile'"
                />
                <el-tab-pane
                    v-if="usableRegister.includes('email')"
                    label="邮箱注册"
                    name="email"
                    @click="currentRegister = 'email'"
                />
            </el-tabs>
            <el-form ref="formRef" size="large" :model="formData" :rules="formRules">
                <!-- 手机号注册 -->
                <el-form-item v-if="currentRegister === 'mobile'" prop="mobile">
                    <el-input v-model="formData.mobile" placeholder="请输入手机号">
                        <template #prepend>
                            <el-select model-value="+86" style="width: 80px">
                                <el-option label="+86" value="+86" />
                            </el-select>
                        </template>
                    </el-input>
                </el-form-item>
                <!-- 邮箱号注册 -->
                <el-form-item v-if="currentRegister === 'email'" prop="email">
                    <el-input v-model="formData.email" placeholder="请输入邮箱号"/>
                </el-form-item>
                <!-- 验证码 -->
                <el-form-item v-if="currentRegister !== 'account'" prop="code">
                    <el-input v-model="formData.code" placeholder="请输入验证码">
                        <template #suffix>
                            <div class="flex justify-center pl-5 leading-5 border-l w-90">
                                <VerifyCode ref="verificationCodeRef" @click-get="onSendSms" />
                            </div>
                        </template>
                    </el-input>
                </el-form-item>
                <!-- 登录账号 -->
                <el-form-item v-if="currentRegister === 'account'" prop="account">
                    <el-input
                        v-model="formData.account"
                        type="text"
                        show-password
                        placeholder="请输入登录账号"
                    />
                </el-form-item>
                <!-- 登录密码 -->
                <el-form-item prop="password">
                    <el-input
                        v-model="formData.password"
                        type="password"
                        show-password
                        placeholder="请输入6~20位数字+字母或符号组合密码"
                    />
                </el-form-item>
                <!-- 确认密码 -->
                <el-form-item prop="password_confirm">
                    <el-input
                        v-model="formData.password_confirm"
                        :loading="isLock"
                        type="password"
                        show-password
                        placeholder="请再次输入密码"
                    />
                </el-form-item>
                <!-- 注册按钮 -->
                <el-form-item>
                    <el-button
                        type="primary"
                        class="w-full h-42"
                        :loading="isLock"
                        @click="onRegisterLock()"
                    >
                        注册
                    </el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 注册关闭 -->
        <el-empty
            v-else
            description="注册服务暂停"
            :image-size="200"
        />

        <!-- 已有账号？ -->
        <div class="flex justify-center cursor-pointer hover:opacity-80">
            已有账号？
            <nuxt-link
                class="text-primary"
                @click="appStore.setPopup(popupEnum.LOGIN)"
            >
                立即登录
            </nuxt-link>
        </div>

        <!-- 隐私协议 -->
        <div v-if="isAgreement" class="protocol">
            <el-checkbox v-model="checked" size="large" />
            <span class="ml-1.5">您注册即同意</span>
            <nuxt-link
                class="text-tx-regular cursor-pointer hover:opacity-80"
                target="_blank"
                :to="`/policy/${policyEnum.SERVICE}`"
            >
                《用户协议》
            </nuxt-link>和
            <nuxt-link
                class="text-tx-regular cursor-pointer hover:opacity-80"
                target="_blank"
                :to="`/policy/${policyEnum.PRIVACY}`"
            >
                《隐私政策》
            </nuxt-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { popupEnum, policyEnum } from '@/enums/app'
import { noticeEnum } from '@/enums/notice'
import useUserStore from '@/stores/user'
import useAppStore from '@/stores/app'
import loginApi from '@/api/login'
import appApi from '@/api/app'

const appStore = useAppStore()
const userStore = useUserStore()

// 注册配置参数
const config = appStore.getLoginConfig.pc

// 是否同意协议
const checked = ref<boolean>(!config?.is_agreement)

// 显示授权协议
const isAgreement = ref<boolean>(config?.is_agreement)

// 可用登录渠道
const usableRegister = ref<string[]>(config?.usable_register)

// 当前注册方式
const currentRegister = ref<string>(usableRegister.value[0] || '')

// 表单参数
const formData = reactive<{
    mobile: string;
    email: string;
    code: string;
    account: string;
    password: string;
    password_confirm: string;
}>({
    mobile: '',
    email: '',
    code: '',
    account: '',
    password: '',
    password_confirm: ''
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
    email: [
        { required: true, message: '请输入邮箱号', trigger: 'blur' },
        {
            pattern: /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
            min: 2,
            max: 30,
            message: '邮箱格式错误',
            trigger: 'blur'
        }
    ],
    code: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { min: 4, max: 20, message: '验证码不正确', trigger: 'blur' }
    ],
    account: [
        { required: true, message: '请输入登录账号', trigger: 'blur' },
        { min: 4, max: 20, message: '账号长度应为4~20个字符', trigger: 'blur'}
    ],
    password: [
        { required: true, message: '请输入6-20位数字+字母或符号组合', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度应为6~20个字符', trigger: 'blur'}
    ],
    password_confirm: [
        {
            trigger: 'blur',
            validator(_rule: any, value: any, callback: any) {
                if (value === '') {
                    callback(new Error('请再次输入密码'))
                } else if (value !== formData.password) {
                    callback(new Error('两次输入的密码不一致'))
                } else {
                    callback()
                }
            }
        }
    ]
}

/**
 * 发验证码
 */
const verificationCodeRef = shallowRef()
const onSendSms = async () => {
    if (!checked.value) {
        feedback.msgError('请阅读《服务协议》与《隐私协议》')
        return
    }

    if (currentRegister.value === 'mobile') {
        await formRef.value?.validateField(['mobile'])
        await appApi.sendSms({
            scene: noticeEnum.MOBILE_REG,
            mobile: formData.mobile
        }).then(() => {
            verificationCodeRef.value?.start()
        }).catch(() => {})
    } else {
        await formRef.value?.validateField(['email'])
        await appApi.sendEmail({
            scene: noticeEnum.EMAIL_REG,
            email: formData.email
        }).then(() => {
            verificationCodeRef.value?.start()
        }).catch(() => {})
    }
}

/**
 * 注册账号
 */
const { lockFn: onRegisterLock, isLock } = useLockFn(async () => {
    if (!checked.value) {
        feedback.msgError('请阅读《服务协议》与《隐私协议》')
        return
    }

    const scene = currentRegister.value
    let account: string = formData.account
    if (scene === 'mobile') {
        account = formData.mobile
    } else if (scene === 'email') {
        account = formData.email
    }

    const params = {
        scene: scene,
        account: account,
        code: formData.code,
        password: formData.password
    }

    await loginApi.register(params).then(async (res: any) => {
        feedback.msgSuccess('注册成功')
        userStore.login(res.token)
        await userStore.getUser()
        setTimeout(() => {
            appStore.setPopup(popupEnum.NULL)
            location.reload()
        }, 1500)
    }).catch(() => {})
})
</script>

<style lang="scss">
.register-popup-container {
    width: 390px;
    .tabs {
        padding-right: 20px;
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
    }

    .protocol {
        display: flex;
        align-items: center;
        padding-left: 15px;
        margin-top: 20px;
        font-size: 13px;
        color: var(--el-text-color-secondary);
        background-color: var(--el-bg-color-page);
        border-radius: 4px;
    }
}
</style>
