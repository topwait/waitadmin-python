<template>
    <div class="w-[360px] px-2">
        <div class="font-semibold mb-4">
            {{ users?.email ? '变更邮箱' : '绑定邮箱' }}
        </div>
        <el-form ref="formRef" size="large" :model="formData" :rules="formRules">
            <el-form-item v-if="users?.email">
                <el-input :value="users.email" placeholder="原邮箱号" :disabled="true" />
            </el-form-item>
            <el-form-item prop="email">
                <el-input v-model="formData.email" placeholder="请输入邮箱号" />
            </el-form-item>
            <el-form-item prop="code">
                <el-input v-model="formData.code" placeholder="请输入验证码">
                    <template #suffix>
                        <div class="flex justify-center leading-5 w-[90px] pl-2.5 border-l border-br">
                            <verify-code ref="verifyCodeRef" @click-get="handleSendEmail" />
                        </div>
                    </template>
                </el-input>
            </el-form-item>
            <ElFormItem>
                <ElButton
                    type="primary"
                    class="w-full h-42"
                    :loading="isLock"
                    @click="handleSubmit"
                >
                    确认
                </ElButton>
            </ElFormItem>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { popupEnum } from '~/enums/app'
import { noticeEnum } from '~/enums/notice'
import useUserStore from '~/stores/user'
import useAppStore from '~/stores/app'
import userApi from '~/api/user'
import appApi from '~/api/app'

const appStore = useAppStore()
const userStore = useUserStore()

// 用户信息
const { users } = toRefs(userStore)

// 表单参数
const formData = reactive({
    code: '',
    email: ''
})

// 表单验证
const formRef = shallowRef<FormInstance>()
const formRules: FormRules = {
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
    ]
}

/**
 * 发验证码
 */
const isSendIng = ref(false)
const verifyCodeRef = shallowRef()
const handleSendEmail = async () => {
    if (!formData.email) {
        return feedback.msgError('请填写接收邮箱号')
    }

    if (formData.email === users.value.email) {
        return feedback.msgError('不能与旧邮箱号相同')
    }

    if (isSendIng.value) {
        return feedback.msgError('操作频繁,请稍后再试')
    }

    await formRef.value?.validateField(['email']).then(async () => {
        let scene = noticeEnum.EMAIL_BIND
        if (users?.value.email) {
            scene = noticeEnum.EMAIL_CHANGE
        }

        isSendIng.value = true
        verifyCodeRef.value?.ing()
        await appApi.sendEmail({
            scene: scene,
            email: formData.email
        }).then(() => {
            feedback.msgSuccess('发送成功')
            verifyCodeRef.value?.start()
        }).catch(() => {
            verifyCodeRef.value?.end()
        }).finally(() => {
            isSendIng.value = false
        })
    }).catch(() => { })
}

/**
 * 绑定邮箱
 */
const { lockFn: handleSubmit, isLock } = useLockFn(async () => {
    if (formData.email === users.value.email) {
        return feedback.msgError('不能与旧邮箱号相同')
    }
    await formRef.value?.validateField().then(async () => {
        await userApi.bindEmail({
            scene: users?.value.email ? 'change' : 'bind',
            email: formData.email,
            code: formData.code
        }).then(async () => {
            feedback.msgSuccess('绑定成功')
            await userStore.getUser()
            setTimeout(() => appStore.setPopup(popupEnum.NULL), 1000)
        }).catch(() => {})
    }).catch(() => {})
}, 1000)
</script>
