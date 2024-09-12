<template>
    <div class="w-[360px] px-2">
        <div class="font-semibold mb-4">
            {{ users?.is_password ? '修改密码' : '设置密码' }}
        </div>
        <el-form ref="formRef" size="large" :model="formData" :rules="formRules">
            <el-form-item label="旧的密码" prop="password_old">
                <el-input v-model="formData.password_old" type="password" placeholder="请输入原始密码" />
            </el-form-item>
            <el-form-item label="新的密码" prop="password">
                <el-input v-model="formData.password" type="password" placeholder="请输入新的密码 (6~20个字符)" />
            </el-form-item>
            <el-form-item label="确认密码" prop="password_confirm">
                <el-input v-model="formData.password_confirm" type="password" placeholder="请再次输入密码" />
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
import useUserStore from '~/stores/user'
import useAppStore from '~/stores/app'
import userApi from '~/api/user'

const appStore = useAppStore()
const userStore = useUserStore()

// 用户信息
const { users } = toRefs(userStore)

// 表单参数
const formData = reactive({
    password: '',
    password_old: '',
    password_confirm: ''
})

// 表单验证
const formRef = shallowRef<FormInstance>()
const formRules: FormRules = {
    password_old: [
        { required: true, message: '请输入原密码', trigger: 'blur' },
        { min: 6, max: 20, message: '原密码错误', trigger: 'blur'}
    ],
    password: [
        { required: true, message: '请输入6-20位数字+字母或符号组合', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度应为6~20个字符', trigger: 'blur'}
    ],
    password_confirm: [
        { required: true, message: '请输再次输入确认密码', trigger: 'blur' },
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
 * 修改密码
 */
const { lockFn: handleSubmit, isLock } = useLockFn(async () => {
    await formRef.value?.validateField().then(async () => {
        await userApi.changePwd({
            new_pwd: formData.password,
            old_pwd: formData.password_old
        }).then(async () => {
            feedback.msgSuccess('修改成功')
            await userStore.getUser()
            setTimeout(() => appStore.setPopup(popupEnum.NULL), 1000)
        }).catch(() => {})
    }).catch(() => {})
}, 1000)
</script>
