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
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="分组名称" prop="name">
                    <el-input v-model="formData.name" placeholder="请输入分组名称" />
                </el-form-item>
                <el-form-item label="分组备注" prop="remarks">
                    <el-input
                        v-model.trim="formData.remarks"
                        type="textarea"
                        :autosize="{ minRows: 4, maxRows: 6 }"
                        maxlength="200"
                        show-word-limit
                    />
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="9999" />
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import userGroupApi from '@/api/users/group'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑分组' : '新增分组'
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: '',       // 分组ID
    name: '',     // 分组名称
    remarks: '',  // 分组备注
    sort: 0       // 分组排序
})

// 表单规则
const formRules = reactive({
    name: [
        { required: true, message: '分组名称不能为空', trigger: ['blur'] },
        { max: 30, message: '分组名称不能大于30个字符', trigger: ['blur'] }
    ],
    remarks: [
        { max: 200, message: '备注内容不能大于200个字符', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await userGroupApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await userGroupApi.add(formData)
            .finally(() => {
                loading.value = false
            })
    }

    feedback.msgSuccess('操作成功')
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
        const data = await userGroupApi.detail(row.id)
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
