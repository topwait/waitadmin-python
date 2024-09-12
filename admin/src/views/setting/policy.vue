<template>
    <el-form ref="formRef">
        <!-- 协议设置 -->
        <el-tabs type="border-card">
            <el-tab-pane label="服务协议">
                <rich-text v-model="formData.service" :height="layoutHeight"/>
            </el-tab-pane>
            <el-tab-pane label="隐私协议">
                <rich-text v-model="formData.privacy" :height="layoutHeight" />
            </el-tab-pane>
            <el-tab-pane label="支付协议">
                <rich-text v-model="formData.payment" :height="layoutHeight"/>
            </el-tab-pane>
        </el-tabs>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:policy:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'
import policyApi from '@/api/setting/policy'
import feedback from '@/utils/feedback'

const appStore = useAppStore()

const layoutHeight = computed(() => {
    const height = appStore.layoutHeight
    return height - 190 < 320 ? 320 : height - 190
})

const loading = ref(false)
const formData = reactive({
    service: '',
    privacy: '',
    payment: ''
})

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await policyApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    loading.value = true
    await policyApi.save(formData)
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
