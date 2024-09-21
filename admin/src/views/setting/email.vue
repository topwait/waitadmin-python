<template>
    <el-form ref="formRef" :rules="rules" :model="formData" label-width="120px">
        <!-- 邮件配置 -->
        <el-card shadow="never" class="!border-none">
            <div class="text-xl font-medium mb-[20px]">邮件设置</div>
            <el-form-item label="发送方式：" prop="smtp_type">
                <div class="w-[380px]">
                    <el-select
                        v-model="formData.smtp_type"
                        placeholder="请选择"
                    >
                        <el-option label="SMTP" value="smtp"/>
                    </el-select>
                </div>
            </el-form-item>
            <el-form-item label="SMTP验证：" prop="verify_type">
                <div class="w-[380px]">
                    <el-select
                        v-model="formData.verify_type"
                        placeholder="请选择"
                    >
                        <el-option label="默认" value="default"/>
                        <el-option label="SSL" value="ssl"/>
                    </el-select>
                </div>
            </el-form-item>
            <el-form-item label="服务器地址：" prop="smtp_host">
                <div class="w-[380px]">
                    <el-input v-model.trim="formData.smtp_host" />
                </div>
            </el-form-item>
            <el-form-item label="服务器端口：" prop="smtp_port">
                <div class="w-[380px]">
                    <el-input v-model.trim="formData.smtp_port" />
                </div>
            </el-form-item>
            <el-form-item label="发件邮箱号：" prop="smtp_user">
                <div class="w-[380px]">
                    <el-input v-model.trim="formData.smtp_user" />
                </div>
            </el-form-item>
            <el-form-item label="邮箱授权码：" prop="smtp_pass">
                <div class="w-[380px]">
                    <el-input v-model.trim="formData.smtp_pass" />
                </div>
            </el-form-item>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:email:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import emailApi from '@/api/setting/email'

const loading = ref(false)
const formRef = ref()
const formData = reactive({
    smtp_type: 'smtp',
    smtp_host: '',
    smtp_port: '',
    smtp_user: '',
    smtp_pass: '',
    from_user: '',
    verify_type: ''
})

// 表单验证
const rules = {
    'smtp_type': [
        { required: true, message: '请选择发送方式', trigger: 'blur' }
    ],
    'verify_type': [
        { required: true, message: '请选择验证类型', trigger: 'blur' }
    ],
    'smtp_host': [
        { max: 100, message: '服务器地址不能超出100个字符', trigger: ['blur'] },
    ],
    'smtp_port': [
        { pattern: /^[0-9]+$/, message: '服务器端口必须是数字', trigger: 'blur' },
        { max: 10, message: '服务器端口不能超出10个字符', trigger: ['blur'] },
    ],
    'smtp_user': [
        { max: 100, message: '发件邮箱号不能超出100个字符', trigger: ['blur'] },
    ],
    'smtp_pass': [
        { max: 100, message: '邮箱授权码不能超出100个字符', trigger: ['blur'] },
    ]
}

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await emailApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()

    loading.value = true
    await emailApi.save(formData)
        .finally(() => {
            setTimeout(() => {
                loading.value = false
            }, 500)
        })

    await queryConfigs()
    feedback.msgSuccess('保存成功')
}

onMounted(async () => {
    await queryConfigs()
})
</script>
