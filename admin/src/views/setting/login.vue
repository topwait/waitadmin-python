<template>
    <el-form ref="formRef" :rules="rules" :model="formData" label-width="120px">
        <!-- 登录设置 -->
        <el-card shadow="never" class="!border-none">
            <div class="text-xl font-medium mb-[20px]">登录设置</div>
            <el-form-item label="显示登录协议：" prop="is_agreement">
                <div>
                    <el-radio-group v-model="formData.is_agreement">
                        <el-radio :value="1">开启</el-radio>
                        <el-radio :value="0">关闭</el-radio>
                    </el-radio-group>
                    <div class="form-tips">用户登录注册时是否显示服务协议和隐私政策阅读功能</div>
                </div>
            </el-form-item>
            <el-form-item label="默认登录方式：" prop="defaults">
                <div>
                    <el-radio-group v-model="formData.defaults">
                        <el-radio value="account">账号登录</el-radio>
                        <el-radio value="mobile">手机登录</el-radio>
                        <el-radio value="wx">微信登录</el-radio>
                    </el-radio-group>
                    <div class="form-tips">被选择为默认的登录方式项必须选一个,否则会显示异常</div>
                </div>
            </el-form-item>
            <el-form-item label="允许注册方式：" prop="register">
                <div>
                    <el-checkbox-group v-model="formData.registers">
                        <el-checkbox value="mobile">手机注册</el-checkbox>
                        <el-checkbox value="email">邮箱注册</el-checkbox>
                    </el-checkbox-group>
                    <div class="form-tips">是否开放注册,如不勾选则不开放注册</div>
                </div>
            </el-form-item>
            <el-form-item label="通用登录方式：" prop="login_modes">
                <div>
                    <el-checkbox-group v-model="formData.login_modes">
                        <el-checkbox value="account">账号密码登录</el-checkbox>
                        <el-checkbox value="mobile">手机短信登录</el-checkbox>
                    </el-checkbox-group>
                    <div class="form-tips">全局系统通用的登录方式,至少勾选一项</div>
                </div>
            </el-form-item>
            <el-form-item label="第三方登录：" prop="login_other">
                <div>
                    <el-checkbox-group v-model="formData.login_other">
                        <el-checkbox value="wx">微信登录</el-checkbox>
                    </el-checkbox-group>
                    <div class="form-tips">支持第三方授权登录,开启后新用户授权即自动注册账号</div>
                </div>
            </el-form-item>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:login:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import feedback from '@/utils/feedback'
import loginApi from '@/api/setting/login'

const loading = ref(false)
const formRef = ref<FormInstance>()
const formData = reactive({
    is_agreement: 0,
    defaults: '',
    registers: [],
    login_modes: [],
    login_other: []
})

// 表单验证
const rules = reactive<FormRules>({
    defaults: [
        { required: true, message: '请选择默认登录方式', trigger: 'blur' }
    ],
    login_modes: [
        {
            required: true,
            validator: (_rule: any, _value: any, callback: any) => {
                const loginModes = formData.login_modes.join('').length
                if (loginModes === 0) {
                    callback(new Error('通用登录方式至少选择一项！'))
                } else {
                    if (formData.login_modes) {
                        if (!formRef.value) {
                            return
                        }
                    }
                    callback()
                }
            },
            trigger: 'change'
        }
    ]
})

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await loginApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()

    loading.value = true
    await loginApi.save(formData)
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
