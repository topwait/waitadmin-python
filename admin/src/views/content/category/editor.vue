<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="400px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="formData.name" maxlength="20" />
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
import articleCateApi from '@/api/content/category'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑分类' : '新增分类'
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: '',       // 分类ID
    name: '',     // 分类名称
    sort: 0,      // 分类排序
    is_disable: 0 // 是否禁用:[0=否, 1=是]
})

// 表单规则
const formRules = reactive({
    name: [
        { required: true, message: '分类名称不能为空', trigger: ['blur'] },
        { max: 20, message: '分类名称不能大于20个字符', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await articleCateApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await articleCateApi.add(formData)
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
        const data = await articleCateApi.detail(row.id)
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
