<template>
    <div class="w-[360px] px-2">
        <div class="font-semibold mb-4">
            {{ users?.mobile ? '变更手机' : '绑定手机' }}
        </div>
        <el-form ref="formRef" size="large" :model="formData" :rules="formRules">
            <el-form-item v-if="users?.mobile">
                <el-input :value="users.mobile" placeholder="原手机号" :disabled="true" />
            </el-form-item>
            <el-form-item prop="mobile">
                <el-input v-model="formData.mobile" placeholder="请输入手机号" />
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
    mobile: '',
    code: ''
})

// 表单验证
const formRef = shallowRef<FormInstance>()
const formRules: FormRules = {
    mobile: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
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
const handleSendSms = async () => {
    if (!formData.mobile) {
        return feedback.msgError('请填写接收手机号')
    }

    if (formData.mobile === users.value.mobile) {
        return feedback.msgError('不能与旧手机号相同')
    }

    if (isSendIng.value) {
        return feedback.msgError('操作频繁,请稍后再试')
    }

    await formRef.value?.validateField(['mobile']).then(async () => {
        let scene = noticeEnum.MOBILE_BIND
        if (users?.value.mobile === 'change') {
            scene = noticeEnum.MOBILE_CHANGE
        }

        isSendIng.value = true
        verifyCodeRef.value?.ing()
        await appApi.sendSms({
            scene: scene,
            mobile: formData.mobile
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
 * 绑定手机
 */
const { lockFn: handleSubmit, isLock } = useLockFn(async () => {
    if (formData.mobile === users.value.mobile) {
        return feedback.msgError('不能与旧手机号相同')
    }
    await formRef.value?.validateField().then(async () => {
        await userApi.bindMobile({
            scene: users?.value.mobile ? 'change' : 'bind',
            mobile: formData.mobile,
            code: formData.code
        }).then(async () => {
            feedback.msgSuccess('绑定成功')
            await userStore.getUser()
            setTimeout(() => appStore.setPopup(popupEnum.NULL), 1000)
        }).catch(() => {})
    }).catch(() => {})
}, 1000)
</script>

<style lang="scss">
.forgot-popup-container {
    width: 390px;
    .el-form {
        .el-input__inner { height: 46px; }
    }
}
</style>