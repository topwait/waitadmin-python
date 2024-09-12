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
                <el-form-item label="友链图标" prop="image">
                    <material-picker
                        v-model="formData.image"
                        :limit="1"
                    />
                </el-form-item>
                <el-form-item label="跳转方式" prop="target">
                    <el-select
                        v-model="formData.target"
                        placeholder="请选择跳转方式"
                        clearable
                    >
                        <el-option label="_blank" value="_blank" />
                        <el-option label="_self" value="_self" />
                        <el-option label="_top" value="_top" />
                        <el-option label="_parent" value="_parent" />
                    </el-select>
                </el-form-item>
                <el-form-item label="友链名称" prop="title">
                    <el-input v-model="formData.title" placeholder="请输入友链名称" maxlength="200" />
                </el-form-item>
                <el-form-item label="跳转链接" prop="url">
                    <el-input v-model="formData.url" placeholder="请输入跳转链接" maxlength="250" />
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="999999" />
                </el-form-item>
                <el-form-item label="状态">
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
import linksApi from '@/api/setting/links'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑友链' : '新增友链'
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: '',        // 管理ID
    title: '',     // 友链名称
    image: '',     // 友链图标
    target: '',    // 跳转方式
    url: '',       // 跳转链接
    sort: 0,       // 排序编号
    is_disable: 0, // 是否禁用:[0=否, 1=是]
})

// 表单规则
const formRules = reactive({
    title: [
        { required: true, message: '友链名称不能为空', trigger: 'blur' },
        { max: 200, message: '友链名称不能大于200个字符', trigger: 'blur' }
    ],
    target: [
        { required: true, message: '请选择跳转方式', trigger: 'blur' },
    ],
    url: [
        { required: true, message: '请填写跳转链接', trigger: 'blur' },
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await linksApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await linksApi.add(formData)
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
        const data = await linksApi.detail(row.id)
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
