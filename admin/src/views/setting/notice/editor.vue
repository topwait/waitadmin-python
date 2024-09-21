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
            <el-form ref="formRef" :model="formData" label-width="80px">
                <el-card class="mb-4" shadow="never">
                    <div class="font-medium mb-3">通知名称</div>
                    <el-form-item label="通知名称:" style="margin: 0;">{{ formData.name }}</el-form-item>
                    <el-form-item label="通知类型:" style="margin: 0;">{{ formData.type }}</el-form-item>
                    <el-form-item label="通知业务:" style="margin: 0;">{{ formData.client }}</el-form-item>
                    <el-form-item label="通知描述:" style="margin: 0;">{{ formData.remarks }}</el-form-item>
                </el-card>
                <el-card class="mb-3" shadow="never" v-if="Object.keys(formData.sys_template).length > 0">
                    <div class="font-medium mb-3">系统通知</div>
                    <el-form-item label="开启状态" prop="sys_template.status" required>
                        <el-radio-group v-model="formData.sys_template.status">
                            <el-radio value="0">关闭</el-radio>
                            <el-radio value="1">开启</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="通知内容" prop="sys_template.content" required>
                        <el-input
                            type="textarea"
                            v-model="formData.sys_template.content"
                            :autosize="{ minRows: 5, maxRows: 5 }"
                        />
                    </el-form-item>
                </el-card>
                <el-card class="mb-3" shadow="never" v-if="Object.keys(formData.ems_template).length > 0">
                    <div class="font-medium mb-3">邮件通知</div>
                    <el-form-item label="开启状态" prop="ems_template.status" required>
                        <el-radio-group v-model="formData.ems_template.status">
                            <el-radio value="0">关闭</el-radio>
                            <el-radio value="1">开启</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="邮件内容" prop="ems_template.content" required>
                        <el-input
                            type="textarea"
                            v-model="formData.ems_template.content"
                            :autosize="{ minRows: 5, maxRows: 5 }"
                        />
                    </el-form-item>
                </el-card>
                <el-card shadow="never" v-if="Object.keys(formData.sms_template).length > 0">
                    <div class="font-medium mb-3">短信通知</div>
                    <el-form-item label="开启状态" prop="sms_template.status" required>
                        <el-radio-group v-model="formData.sms_template.status">
                            <el-radio value="0">关闭</el-radio>
                            <el-radio value="1">开启</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="模板编号" prop="sms_template.template_code" required>
                        <el-input
                            v-model="formData.sms_template.template_code"
                            placeholder="请输入模板ID"
                        />
                    </el-form-item>
                    <el-form-item label="短信内容" prop="sms_template.content" required>
                        <el-input
                            type="textarea"
                            v-model="formData.sms_template.content"
                            :autosize="{ minRows: 5, maxRows: 5 }"
                        />
                    </el-form-item>
                </el-card>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import noticeApi from '@/api/setting/notice'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '设置' : ''
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive({
    id: 0,
    scene: 0,
    name: '',
    type: '',
    client: '',
    remarks: '',
    variable: {},
    sys_template: {content: '', template_code: '', status: 0},
    ems_template: {content: '', template_code: '', status: 0},
    sms_template: {content: '', template_code: '', status: 0}
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await noticeApi.save(formData)
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
        const data = await noticeApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                // @ts-ignore
                formData[key] = data[key]
            }
        }
    }
}

defineExpose({
    open
})
</script>
