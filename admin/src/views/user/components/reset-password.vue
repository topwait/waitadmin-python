<template>
    <popup
        :show="true"
        :title="'重置密码'"
        :loading="loading"
        :async-close="true"
        width="500px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <el-form @submit.prevent>
            <el-form-item label="密码设置">
                <el-input type="password" v-model="formData.password" show-password />
            </el-form-item>
        </el-form>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import userApi from '@/api/users/user'

const emits = defineEmits(['close', 'success'])

const props = defineProps({
    user_id: {
        type: Number,
        default: 0
    }
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive({
    password: ''
})

/**
 * 提交表单
 */
const handleSubmit = async () => {
    loading.value = true
    await userApi.resetPassword(props.user_id, formData.password)
        .finally(() => {
            loading.value = false
        })

    feedback.msgSuccess('重置成功')
    emits('close')
    emits('success')
}
</script>
