<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="500px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
                <el-form-item label="短信渠道" prop="name">
                    <el-input
                        v-model="formData.name"
                        maxlength="20"
                        clearable
                        :disabled="true"
                    />
                </el-form-item>
                <el-form-item label="短信签名" prop="params.sign">
                    <el-input
                        v-model="formData.params.sign"
                        maxlength="50"
                        clearable
                    />
                </el-form-item>
                <el-form-item v-if="formData.alias === 'tencent'" label="APP_ID" prop="params.app_id">
                    <el-input
                        v-model="formData.params.app_id"
                        maxlength="800"
                        clearable
                    />
                </el-form-item>
                <el-form-item label="APP_KEY" prop="params.acc_key">
                    <el-input
                        v-model="formData.params.acc_key"
                        maxlength="800"
                        clearable
                    />
                </el-form-item>
                <el-form-item label="SECRET_KEY" prop="params.acc_secret">
                    <el-input
                        v-model="formData.params.acc_secret"
                        maxlength="800"
                        clearable
                    />
                </el-form-item>
                <el-form-item label="状态" prop="status">
                    <el-radio-group v-model="formData.status">
                        <el-radio :value="1">启用</el-radio>
                        <el-radio :value="0">停用</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import smsApi from '@/api/setting/sms'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '设置' : ''
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    alias: '',
    name: '',
    status: 0,
    params: {
        sign: '',
        app_id: '',
        acc_key: '',
        acc_secret: ''
    }
})

// 表单规则
const formRules: any = reactive({
    'params.sign': [
        { max: 100, message: '短信签名不能大于100个字符', trigger: ['blur'] }
    ],
    'params.app_id': [
        { max: 200, message: 'APP_ID不能大于200个字符', trigger: ['blur'] }
    ],
    'params.acc_key': [
        { max: 200, message: 'APP_KEY不能大于200个字符', trigger: ['blur'] }
    ],
    'params.acc_secret': [
        { max: 200, message: 'SECRET_KEY不能大于200个字符', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await smsApi.save(formData)
            .finally(() => {
                loading.value = false
            })
    }

    feedback.msgSuccess('设置成功')
    emits('close')
    emits('success')
}

/**
 * 打开表单
 *
 * @param {string} type
 * @param {any} row
 * @returns {Promise<void>}
 */
const open = async (type: string, row?: any): Promise<void> => {
    showMode.value = type
    showEdit.value = true

    if (type === 'edit') {
        const data = await smsApi.detail(row.alias)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                formData[key] = data[key]
            }
        }
    }
}

defineExpose({
    open
})
</script>
