<template>
    <div class="forgot-popup-container">
        <div class="px-[20px]">
            <h3 class="text-2xl font-semibold mb-3">找回密码</h3>
            <el-form ref="formRef" class="mt-[30px]" size="large" :model="formData" :rules="formRules">
                <el-form-item prop="account">
                    <el-input v-model="formData.account" placeholder="请输入账号">
                        <template #prepend>
                            <ElSelect v-model="currentForgot" style="width: 80px">
                                <ElOption label="手机" value="mobile" />
                                <ElOption label="邮箱" value="email" />
                            </ElSelect>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="code">
                    <el-input v-model="formData.code" placeholder="请输入验证码">
                        <template #suffix>
                            <div class="flex justify-center leading-5 border-l w-[90px]">
                                <VerifyCode ref="verificationCodeRef" @click-get="onSendSms" />
                            </div>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        v-model="formData.password"
                        type="password"
                        show-password
                        placeholder="请输入6~20位数字+字母或符号组合密码"
                    />
                </el-form-item>
                <el-form-item prop="password_confirm">
                    <el-input
                        v-model="formData.password_confirm"
                        type="password"
                        show-password
                        placeholder="请再次输入密码"
                    />
                </el-form-item>
                <el-form-item>
                    <el-button
                        type="primary"
                        class="w-full h-42"
                        :loading="isLock"
                        @click="handleSubmit"
                    >
                        确认
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="flex justify-center mb-[20px]">
            <NuxtLink
                class="text-primary-default cursor-pointer"
                @click="appStore.setPopup(popupEnum.LOGIN)"
            >
                返回登录
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { noticeEnum } from '~/enums/notice'
import { popupEnum } from '~/enums/app'
import useAppStore from '~/stores/app'
import userApi from '~/api/user'
import appApi from '~/api/app'

const appStore = useAppStore()

const currentForgot = ref('mobile')

// 表单参数
const formData = reactive({
    code: '',
    account: '',
    password: '',
    password_confirm: ''
})

// 表单验证
const formRef = shallowRef<FormInstance>()
const formRules: FormRules = {
    account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    code: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { min: 4, max: 20, message: '验证码不正确', trigger: 'blur' }
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
const isSendIng = ref(false)
const verifyCodeRef = shallowRef()
const onSendSms = async () => {
    if (isSendIng.value) {
        return feedback.msgError('操作频繁,请稍后再试')
    }

    if (currentForgot.value === 'mobile') {
        await formRef.value?.validateField(['account']).then(async () => {
            isSendIng.value = true
            verifyCodeRef.value?.ing()
            await appApi.sendSms({
                scene: noticeEnum.FORGET_PWD,
                mobile: formData.account
            }).then(() => {
                feedback.msgSuccess('发送成功')
                verifyCodeRef.value?.start()
            }).catch((e) => {
                verifyCodeRef.value?.end()
                feedback.msgError(e.message)
            }).finally(() => {
                isSendIng.value = false
            })
        }).catch(() => {})
    } else {
        await formRef.value?.validateField(['account']).then(async () => {
            isSendIng.value = true
            verifyCodeRef.value?.ing()
            await appApi.sendEmail({
                scene: noticeEnum.FORGET_PWD,
                email: formData.account
            }).then(() => {
                feedback.msgSuccess('发送成功')
                verifyCodeRef.value?.start()
            }).catch((e) => {
                verifyCodeRef.value?.end()
                feedback.msgError(e.message)
            }).finally(() => {
                isSendIng.value = false
            })
        }).catch(() => {})
    }
}

/**
 * 重设密码
 */
const { lockFn: handleSubmit, isLock } = useLockFn(async () => {
    await formRef.value?.validateField().then(async () => {
        await userApi.forgetPwd({
            account: formData.account,
            password: formData.password,
            code: formData.code,
        }).then(() => {
            feedback.msgSuccess('更改成功')
            setTimeout(() => appStore.setPopup(popupEnum.LOGIN), 1000)
        }).catch(() => {})
    }).catch(() => {})
}, 1000)
</script>

<style lang="scss">
.forgot-popup-container {
    width: 390px;
    .el-form {
        .el-input__inner { height: 46px; }
        .el-select__wrapper { box-shadow: none !important; }
    }
}
</style>