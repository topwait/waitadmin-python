<template>
    <popup
        :show="true"
        :title="'调整余额'"
        :loading="loading"
        :async-close="true"
        width="500px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form
                ref="formRef"
                label-width="120px"
                :model="formData"
                :rules="formRules"
                @submit.prevent
            >
                <el-form-item label="当前余额">
                    {{ value }}
                </el-form-item>
                <el-form-item label="变更方式" required prop="action">
                    <el-radio-group v-model="formData.action">
                        <el-radio value="inc">增加</el-radio>
                        <el-radio value="dec">扣减</el-radio>
                        <el-radio value="final">最终</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="调整的数值" required prop="amount">
                    <el-input
                        v-model="formData.amount"
                        placeholder="请输入要变更的数值"
                        type="number"
                    />
                </el-form-item>
                <el-form-item :label="`调整后的值`">
                    fff
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script lang="ts" setup>
import type { FormInstance, FormRules } from 'element-plus'
import feedback from '@/utils/feedback'
import userApi from '@/api/users/user'

const emits = defineEmits(['success', 'close'])
const formRef = shallowRef<FormInstance>()

const props = defineProps({
    user_id: {
        type: Number,
        default: 0
    },
    value: {
        type: [Number, String],
        required: true
    }
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive({
    user_id: 0,    // 用户ID
    action: 'inc', // 变更方式: [inc=增加, dec=减少, final=最终]
    amount: 0,     // 变更数值
    remark: ''     // 备注信息
})

// 表单规则
const formRules: FormRules = {
    amount: [
        {
            required: true,
            message: '请输入变更的数值'
        }
    ]
}

/**
 * 提交表单
 */
const handleSubmit = async () => {
    formData.user_id = props.user_id

    loading.value = true
    await userApi.adjustAccount(formData)
        .finally(() => {
            loading.value = false
        })

    feedback.msgSuccess('调整成功')
    emits('close')
    emits('success')
}
</script>
