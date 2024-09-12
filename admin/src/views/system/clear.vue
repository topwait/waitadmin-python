<template>
    <div>
        <el-form :model="formData" label-width="120px">
            <el-card shadow="never" class="!border-none">
                <div class="text-xl font-medium mb-[20px]">清除缓存</div>
                <el-form-item label="数据缓存：" prop="checked">
                    <el-checkbox v-model="formData.system" label="系统缓存" value="system" size="large" />
                    <el-checkbox v-model="formData.login" label="登录缓存" value="login" size="large" />
                </el-form-item>
                <el-form-item>
                    <el-button
                        v-perms="['system:clear:clean']"
                        :loading="loading"
                        type="primary"
                        @click="handleSubmit"
                    >立即清理</el-button>
                </el-form-item>
            </el-card>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import clearApi from '@/api/system/clear'

const loading = ref(false)
const formData = reactive({
    system: false,
    login: false
})

/**
 * 提交表单
 */
const handleSubmit = async () => {
    if (!formData.system && !formData.login) {
        return feedback.msgError('请至少选择一个清理选项')
    }

    loading.value = true
    await clearApi.clean(formData)
        .finally(() => {
            setTimeout(() => {
                loading.value = false
            }, 500)
        })

    feedback.msgSuccess('清理成功')
}
</script>

<style scoped lang="scss"></style>
