<template>
    <el-form :model="formData" label-width="120px">
        <!-- 登录设置 -->
        <el-card shadow="never" class="border-none!">
            <div class="text-xl font-medium mb-5">登录设置</div>
            <el-form-item label="显示授权协议：" prop="pc.is_agreement" required>
                <div>
                    <el-radio-group v-model="formData.pc.is_agreement">
                        <el-radio :value="true">开启</el-radio>
                        <el-radio :value="false">关闭</el-radio>
                    </el-radio-group>
                    <div class="form-tips">用户登录注册时是否显示服务协议和隐私政策阅读功能</div>
                </div>
            </el-form-item>
            <el-form-item label="默认登录方式：" prop="pc.default_method" required>
                <div>
                    <el-radio-group v-model="formData.pc.default_method">
                        <el-radio value="account">账号登录</el-radio>
                        <el-radio value="mobile">手机登录</el-radio>
                        <el-radio value="wx">微信登录</el-radio>
                    </el-radio-group>
                    <div class="form-tips">被选择为默认的登录方式项必须选一个,否则会显示异常</div>
                </div>
            </el-form-item>
            <el-form-item label="可用登录方式：" prop="pc.usable_channel">
                <div>
                    <el-checkbox-group v-model="formData.pc.usable_channel">
                        <el-checkbox value="account">账号登录</el-checkbox>
                        <el-checkbox value="mobile">手机登录</el-checkbox>
                        <el-checkbox value="wx">微信登录</el-checkbox>
                    </el-checkbox-group>
                    <div class="form-tips">可用登录方式,如不勾选则不开放登录</div>
                </div>
            </el-form-item>
            <el-form-item label="允许注册方式：" prop="pc.usable_register">
                <div>
                    <el-checkbox-group v-model="formData.pc.usable_register">
                        <el-checkbox value="account">账号注册</el-checkbox>
                        <el-checkbox value="mobile">手机注册</el-checkbox>
                        <el-checkbox value="email">邮箱注册</el-checkbox>
                    </el-checkbox-group>
                    <div class="form-tips">是否开放注册,如不勾选则不开放注册</div>
                </div>
            </el-form-item>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="border-none! mt-4">
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
import feedback from '@/utils/feedback'
import loginApi from '@/api/setting/login'

const loading = ref<boolean>(false)
const formData = reactive({
    pc: {
        is_agreement: true,
        default_method: 'account',
        usable_channel: [],
        usable_register: []
    }
})

/**
 * 查询配置参数
 *
 * @returns {Promise<void>}
 * @author zero
 */
const queryConfigs = async (): Promise<void> => {
    const data = await loginApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 *
 * @returns {Promise<void>}
 * @author zero
 */
const handleSubmit = async (): Promise<void> => {
    try {
        loading.value = true
        await loginApi.save(formData)
            .finally(() => {
                setTimeout(() => {
                    loading.value = false
                }, 500)
            })

        await queryConfigs()
        feedback.msgSuccess('保存成功')
    } catch {}
}

onMounted(async () => {
    await queryConfigs()
})
</script>
