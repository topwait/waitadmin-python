<template>
    <div>
        <!-- 账号信息 -->
        <el-card class="!border-none" shadow="never">
            <el-form
                ref="formRef"
                :model="formData"
                :rules="rules"
                label-width="100px"
            >
                <el-form-item label="头像：" prop="avatar">
                    <upload-cropper-select v-model="formData.avatar" />
                </el-form-item>
                <el-form-item label="角色：" prop="role" required>
                    <div class="w-80">
                        <el-input v-model="formData.role" disabled />
                    </div>
                </el-form-item>
                <el-form-item label="账号：" prop="username">
                    <div class="w-80">
                        <el-input v-model="formData.username" disabled />
                    </div>
                </el-form-item>
                <el-form-item label="昵称：" prop="nickname">
                    <div class="w-80">
                        <el-input v-model="formData.nickname" placeholder="请输入昵称" />
                    </div>
                </el-form-item>
                <el-form-item label="联系电话：" prop="mobile">
                    <div class="w-80">
                        <el-input v-model="formData.mobile" placeholder="请输入联系电话" />
                    </div>
                </el-form-item>
                <el-form-item label="电子邮箱：" prop="email">
                    <div class="w-80">
                        <el-input v-model="formData.email" placeholder="请输入电子邮箱" />
                    </div>
                </el-form-item>
                <el-form-item label="当前密码：" prop="password_old">
                    <div class="w-80">
                        <el-input
                            v-model.trim="formData.password_old"
                            placeholder="修改密码时必填, 不修改密码时留空"
                            type="password"
                            show-password
                        />
                    </div>
                </el-form-item>
                <el-form-item label="新的密码：" prop="password">
                    <div class="w-80">
                        <el-input
                            v-model.trim="formData.password"
                            placeholder="修改密码时必填, 不修改密码时留空"
                            type="password"
                            show-password
                        />
                    </div>
                </el-form-item>
                <el-form-item label="确定密码：" prop="password_confirm">
                    <div class="w-80">
                        <el-input
                            v-model.trim="formData.password_confirm"
                            placeholder="修改密码时必填, 不修改密码时留空"
                            type="password"
                            show-password
                        />
                    </div>
                </el-form-item>
            </el-form>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存</el-button>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import type { FormInstance } from 'element-plus'
import feedback from '@/utils/feedback'
import useUserStore from '@/stores/modules/user'
import authAdminApi from '@/api/auth/admin'

const userStore = useUserStore()

const loading = ref<boolean>(false)
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive({
    avatar: '',          // 头像
    role: '',            // 角色
    nickname: '',        // 昵称
    username: '',        // 账号
    mobile: '',          // 联系电话
    email: '',           // 电子邮箱
    password: '',        // 新的密码
    password_old: '',    // 当前密码
    password_confirm: '' // 确定密码
})

// 表单规则
const rules = reactive<object>({
    avatar: [
        { required: true, message: '头像不能为空', trigger: ['change'] }
    ],
    username: [
        { required: true, message: '登录账号不能为空', trigger: 'blur' },
        { max: 20, message: '登录账号不能大于20个字符', trigger: 'blur' }
    ],
    nickname: [
        { required: true, message: '用户昵称不能为空', trigger: 'blur' },
        { max: 20, message: '用户昵称不能大于20个字符', trigger: 'blur' }
    ]
})

/**
 * 获取用户
 */
const getUserInfo = (): void => {
    const userInfo = userStore.users
    for (const key in formData) {
        // @ts-ignore
        formData[key] = userInfo[key]
    }
}

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    if (formData.password_old || formData.password || formData.password_confirm) {
        if (!formData.password_old) {
            return feedback.msgError('请输入当前密码')
        }

        if (!formData.password) {
            return feedback.msgError('请输入新的密码')
        }

        if (!formData.password_confirm) {
            return feedback.msgError('请输入确定密码')
        }

        if (formData.password_confirm !== formData.password) {
            return feedback.msgError('两次输入的密码不一样')
        }

        if (formData.password_old && formData.password && formData.password_confirm) {
            if (formData.password_old.length < 6 || formData.password_old.length > 20) {
                return feedback.msgError('密码长度在6到20之间')
            }
            if (formData.password.length < 6 || formData.password.length > 20) {
                return feedback.msgError('密码长度在6到20之间')
            }
            if (formData.password_confirm.length < 6 || formData.password_confirm.length > 20) {
                return feedback.msgError('密码长度在6到20之间')
            }
        }
    }
    loading.value = true
    await authAdminApi.setInfo(formData)
        .finally(() => {
            loading.value = false
        })

    feedback.msgSuccess('保存成功')
    await userStore.getUserInfo()
}

onMounted(() => {
    getUserInfo()
})
</script>
