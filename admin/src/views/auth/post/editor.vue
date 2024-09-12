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
                <el-form-item label="岗位编号" prop="code">
                    <el-input v-model="formData.code" placeholder="请输入岗位编号" maxlength="20" />
                </el-form-item>
                <el-form-item label="岗位名称" prop="name">
                    <el-input v-model="formData.name" placeholder="请输入岗位名称" maxlength="20" />
                </el-form-item>
                <el-form-item label="岗位备注" prop="remarks">
                    <el-input
                        type="textarea"
                        :rows="5"
                        v-model.trim="formData.remarks"
                        show-word-limit
                    />
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="9999" />
                </el-form-item>
                <el-form-item label="状态" prop="is_disable">
                    <el-radio-group v-model="formData.is_disable">
                        <el-radio :value="0">正常</el-radio>
                        <el-radio :value="1">停用</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import authPostApi from '@/api/auth/post'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑岗位' : '新增岗位'
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: '',       // 岗位ID
    code: '',     // 岗位编号
    name: '',     // 岗位名称
    remarks: '',  // 岗位备注
    sort: 0,      // 岗位排序
    is_disable: 0 // 是否禁用:[0=否, 1=是]
})

// 表单规则
const formRules = reactive({
    code: [
        { required: true, message: '岗位编号不能为空', trigger: ['blur'] },
        { min: 2, max: 10, message: '岗位编号长度必须介于 2 和 20 之间', trigger: ['blur'] }
    ],
    name: [
        { required: true, message: '岗位名称不能为空', trigger: ['blur'] },
        { min: 4, max: 20, message: '岗位长度必须介于 2 和 30 之间', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await authPostApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await authPostApi.add(formData)
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
        const data = await authPostApi.detail(row.id)
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
